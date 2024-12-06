from pathlib import Path
from textwrap import dedent
from utils import assert_exists, chmodx, mkdirp
from common import MODELS, LANGUAGES, SPLITS, STRATEGIES, VERSIONS

RESCORE_PY = Path("src") / "rescore.py"
RUN_EXPERIMENT_PY = Path("src") / "run_experiment.py"

assert_exists(RUN_EXPERIMENT_PY)
assert_exists(RESCORE_PY)

def generate_submit_all_sh(path: Path, slurm_files: list):
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
                        # Check if input file exists
                        prompts_file = Path("data") / "output" / "prompts" / lang / split / strategy / version / "prompts.json"
                        assert_exists(prompts_file)

                        # Create output folder for task
                        task_output_folder = Path("data") / "output" / "results" / model / lang / split / strategy / version
                        mkdirp(task_output_folder)
                        task_output_folders.append(task_output_folder)

                        # Determine output locations
                        task_output_file = task_output_folder / "results.json"
                        task_score_file = task_output_folder / "score.json"

                        PARTITION = "ckpt-g2"

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
                            conda activate thesis

                            export HF_HOME=/gscratch/clmbr/amelie/.cache

                            python3 {RUN_EXPERIMENT_PY.absolute()} \\
                                --prompts-file {prompts_file.absolute()} \\
                                --model {model} \\
                                --output {task_output_file.absolute()}

                            {get_python_rescore_command(task_output_file.parent.absolute())}
                        """))
    
    submit_all_sh = script_folder / "slurm-submit-all.sh"
    generate_submit_all_sh(submit_all_sh, slurm_files)
    all_submit_alls.append(submit_all_sh)

with open(Path("scripts") / "generated" / "slurm" / "submit-all-models.sh", "w") as f:
    f.write("#!/bin/bash\n")
    for sh_file in all_submit_alls:
        f.write(f"{sh_file}\n")
