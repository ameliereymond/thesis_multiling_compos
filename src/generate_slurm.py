import os
from pathlib import Path
from textwrap import dedent
import os
import stat

def assert_exists(file_path: Path):
    if not file_path.exists():
        raise Exception(f"Expected {file_path.absolute()} to exist")
    
def chmodx(file_path: Path):
    st = os.stat(file_path).st_mode
    os.chmod(file_path, st | stat.S_IEXEC)

def generate_submit_all_sh(path: Path, slurm_files: list):
    print(f"Creating {path.absolute()}")
    with open(path, "w") as f:
        f.write("#!/bin/bash\n")
        for slurm in slurm_files:
            f.write(f"sbatch {slurm}\n")
    chmodx(path)

def get_python_rescore_command(folder: Path):
    rescore_py = Path("src") / "rescore.py"
    assert_exists(rescore_py)
    return f"python {rescore_py.absolute()} {folder.absolute()}"

def generate_rescore_all(rescore_script_path: Path, results_folder: Path):
    """
    Generates a script at rescore_script_path that rescores all results.json files under results_folder
    """

    print(f"Creating {rescore_script_path.absolute()}")
    with open(rescore_script_path, "w") as f:
        f.write("#!/bin/bash\n")
        f.write(get_python_rescore_command(results_folder))
    
    chmodx(rescore_script_path)

models = {
    "aya": { "gpu_count": 2 },
    "bloom": { "gpu_count": 2 },
    "bloomz": { "gpu_count": 1 },
    "bloomz-mt": { "gpu_count": 1 },
    "llama-3-8B": { "gpu_count": 1 },
    "llama-3-8B-instruct": { "gpu_count": 1 },
    "xglm": { "gpu_count": 1 }
}

splits = ["mcd1", "mcd2", "mcd3", "add_prim_jump", "add_prim_turn_left", "length_split", "simple"]
langs = ["en", "fr", "cmn", "hin", "ru"]


script_file = Path("src") / "run_experiment.py"
assert_exists(script_file)

# Generate a rescore script that will rescore ALL output
generate_rescore_all(
    rescore_script_path = Path("scripts") / "generated" / "slurm" / "rescore-all.sh",
    results_folder = Path("data") / "output" / "results")


for model, settings in models.items():
    script_folder = Path("scripts") / "generated" / "slurm" / model
    os.makedirs(script_folder.absolute(), exist_ok=True)

    # Generate script to rescore a single model output
    model_output_folder = Path("data") / "output" / "results" / model
    generate_rescore_all(script_folder / "rescore-all.sh", model_output_folder)

    # Create all slurm jobs
    slurm_files = []
    task_output_folders = []
    for lang in langs:
        for split in splits:
            slurm_file = script_folder / f"run-{model}-{lang}-{split}.slurm"
            slurm_files.append(slurm_file.absolute())

            print(f"Creating {slurm_file.absolute()}")
            with open(slurm_file, "w") as f:
                # Create output folder for task
                task_output_folder = Path("data") / "output" / "results" / model / lang / split
                os.makedirs(task_output_folder.absolute(), exist_ok=True)
                task_output_folders.append(task_output_folder)

                # Determine file locations
                input_data_folder = Path("data") / "output" / "datasets" / lang / split
                train_data = input_data_folder / "train.txt"
                test_data = input_data_folder / "test.txt"

                task_output_file = task_output_folder / "results.json"
                task_score_file = task_output_folder / "score.json"
                
                assert_exists(train_data)
                assert_exists(test_data)
                
                # Create slurm script for task
                special_handling = ""
                if split == "add_prim_jump" or split == "add_prim_turn_left":
                    special_handling = f"--special-handling {split}"

                f.write("#!/bin/bash\n")
                f.write(dedent(f"""
                    #SBATCH --account=clmbr
                    #SBATCH --job-name={model}-{lang}-{split}
                    #SBATCH --partition=gpu-l40
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

                    python3 {script_file.absolute()} \\
                        --model {model} \\
                        --train {train_data.absolute()} \\
                        --test {test_data.absolute()} \\
                        --output {task_output_file.absolute()} \\
                        {special_handling}

                    {get_python_rescore_command(task_output_file.parent.absolute())}
                """))
    
    generate_submit_all_sh(script_folder / "slurm-submit-all.sh", slurm_files)