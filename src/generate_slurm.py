from pathlib import Path
from textwrap import dedent
from utils import assert_exists, chmodx, mkdirp
from common import MODELS, LANGUAGES, SPLITS, STRATEGIES, VERSIONS
from typing import List

# Specifies which SLURM partition to send jobs to
#PARTITION = "ckpt-g2"
PARTITION = "gpu-l40"

# When running batched, specifies how many batches the SLURM jobs should
# be split into
NUMBER_BATCHES = 1

# Path to rescore python script
RESCORE_PY = Path("src") / "rescore.py"

# Path to experiment python script
RUN_EXPERIMENT_PY = Path("src") / "run_experiment.py"


assert_exists(RUN_EXPERIMENT_PY)
assert_exists(RESCORE_PY)

def chunk_array(arr, chunk_size):
    """Splits an array into chunks of the specified size.

    Args:
        arr: The array to split.
        chunk_size: The size of each chunk.

    Returns:
        A list of arrays, where each array is a chunk of the original array.
    """
    return [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]


def generate_submit_all_sh(path: Path, slurm_files: List[Path]):
    print(f"Creating {path.absolute()}")
    with open(path, "w") as f:
        f.write("#!/bin/bash\n")
        for slurm in slurm_files:
            f.write(f"sbatch {slurm}\n")
    chmodx(path)

def get_python_rescore_command(folder: Path):
    return f"python {RESCORE_PY.absolute()} {folder.absolute()}"

def generate_rescore_all(rescore_script_path: Path, results_folder: Path):
    """
    Generates a script at rescore_script_path that rescores all results.json files under results_folder
    """

    mkdirp(rescore_script_path.parent)

    print(f"Creating {rescore_script_path.absolute()}")
    with open(rescore_script_path, "w") as f:
        f.write("#!/bin/bash\n")
        f.write(get_python_rescore_command(results_folder))
    
    chmodx(rescore_script_path)


# Generate a rescore script that will rescore ALL output
generate_rescore_all(
    rescore_script_path = Path("scripts") / "generated" / "slurm" / "rescore-all.sh",
    results_folder = Path("data") / "output" / "results")

# Generate one slurm file per task
all_submit_alls = []
for model, settings in MODELS.items():
    script_folder = Path("scripts") / "generated" / "slurm" / model
    mkdirp(script_folder)

    # Generate script to rescore a single model output
    model_output_folder = Path("data") / "output" / "results" / model
    generate_rescore_all(script_folder / "rescore-all.sh", model_output_folder)

    # Create all slurm jobs
    slurm_files = []
    task_output_folders = []
    for lang in LANGUAGES:
        for split in SPLITS:
            for strategy in STRATEGIES:
                for version in VERSIONS.keys():
                    run_id = f"{model}-{lang}-{split}-{strategy}-{version}"
                    
                    slurm_file = script_folder / f"run-{run_id}.slurm"
                    slurm_files.append(slurm_file.absolute())
                    
                    print(f"Creating {slurm_file.absolute()}")
                    with open(slurm_file, "w") as f:
                        prompt_style = settings["prompt_style"] if "prompt_style" in settings else "string"
                        if prompt_style == "openai":
                            filename = "prompts-openai.json"
                        elif prompt_style == "llama":
                            filename = "prompts-llama.json"
                        else:
                            filename = "prompts-string.json"

                        # Check if input file exists
                        prompts_file = Path("data") / "output" / "prompts" / lang / split / strategy / version / filename
                        assert_exists(prompts_file)

                        # Create output folder for task
                        task_output_folder = Path("data") / "output" / "results" / model / lang / split / strategy / version
                        mkdirp(task_output_folder)
                        task_output_folders.append(task_output_folder)

                        # Determine output locations
                        task_output_file = task_output_folder / "results.json"
                        task_score_file = task_output_folder / "score.json"

                        # Write slurm file contents
                        f.write("#!/bin/bash\n")
                        f.write(dedent(f"""
                            #SBATCH --account=clmbr
                            #SBATCH --job-name={run_id}
                            #SBATCH --partition={PARTITION}
                            #SBATCH --nodes=1
                            #SBATCH --ntasks-per-node=1
                            #SBATCH --gpus-per-node={settings["gpu_count"]}
                            #SBATCH --mem=48G
                            #SBATCH --time=05:00:00
                            #SBATCH -o {task_output_folder.absolute()}/%x_%j.out

                            conda init bash
                            source ~/.bashrc
                            conda activate misinfo

                            export HF_HOME=/gscratch/clmbr/amelie/.cache

                            python3 {RUN_EXPERIMENT_PY.absolute()} \\
                                --prompts-file {prompts_file.absolute()} \\
                                --model {model} \\
                                --output {task_output_file.absolute()}

                            {get_python_rescore_command(task_output_file.parent.absolute())}
                        """))
    
    # Generate slurm jobs that run batches of tasks together on a single node
    # This helps keep the number of concurrently running tasks under control
    # (e.g. for rate limited APIs)
    chunk_size = max(1, len(slurm_files) // NUMBER_BATCHES)
    batched_slurm_files = []
    for i, batch in enumerate(chunk_array(slurm_files, chunk_size)):
        slurm_file = script_folder / f"batch-{i}.slurm"
        batched_slurm_files.append(slurm_file)
        print(f"Creating {slurm_file.absolute()}")

        task_output_folder = Path("data") / "output" / "results" / model
        
        with open(slurm_file, "w") as f:
            f.write("#!/bin/bash\n")
            f.write(dedent(f"""
                #SBATCH --account=clmbr
                #SBATCH --job-name={model}-batch-{i}
                #SBATCH --partition={PARTITION}
                #SBATCH --nodes=1
                #SBATCH --ntasks-per-node=1
                #SBATCH --gpus-per-node={settings["gpu_count"]}
                #SBATCH --mem=48G
                #SBATCH --time=05:00:00
                #SBATCH -o {task_output_folder.absolute()}/%x_%j.out
            """))

            for file in batch:
                f.write(f"bash {file}\n")
    
    generate_submit_all_sh(script_folder / "slurm-submit-all-batched.sh", batched_slurm_files)
    generate_submit_all_sh(script_folder / "slurm-submit-all.sh", slurm_files)
    all_submit_alls.append(script_folder / "slurm-submit-all.sh")

# Generate a script that will submit all the slurm tasks for all the models
submit_all_models_sh = Path("scripts") / "generated" / "slurm" / "submit-all-models.sh"
with open(submit_all_models_sh, "w") as f:
    f.write("#!/bin/bash\n")
    for sh_file in all_submit_alls:
        f.write(f"{sh_file.absolute()}\n")
chmodx(submit_all_models_sh)