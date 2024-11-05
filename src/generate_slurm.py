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
    os.chmod(submit_all_sh, st | stat.S_IEXEC)

models = ["bloomz"]
splits = ["mcd1", "mcd2", "mcd3", "add_prim_jump", "add_prim_turn_left", "length_split", "simple"]
langs = ["en", "fr", "cmn", "hin", "ru"]

for model in models:
    script_file = Path("src") / f"experiment_{model}.py"
    assert_exists(script_file)

    score_file = Path("src") / "rescore.py"
    assert_exists(score_file)

    output_folder = Path("scripts") / "generated" / "slurm" / model
    os.makedirs(output_folder.absolute(), exist_ok=True)

    # Create all slurm jobs
    slurm_files = []
    task_output_folders = []
    for lang in langs:
        for split in splits:
            slurm_file = output_folder / f"run-{model}-{lang}-{split}.slurm"
            slurm_files.append(slurm_file.absolute())

            print(f"Creating {slurm_file.absolute()}")
            with open(slurm_file, "w") as f:
                # Create output folder for task
                task_output_folder = Path("data") / "output" / "results" / model / lang / split
                os.makedirs(output_folder.absolute(), exist_ok=True)
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
                    #SBATCH --gpus-per-node=1
                    #SBATCH --mem=48G
                    #SBATCH --time=05:00:00
                    #SBATCH -o {task_output_folder.absolute()}/%x_%j.out

                    conda init bash
                    conda activate thesis

                    export HF_HOME=/gscratch/clmbr/amelie/.cache

                    python {script_file.absolute()} \\
                        --train {train_data.absolute()} \\
                        --test {test_data.absolute()} \\
                        --output {task_output_file.absolute()} \\
                        {special_handling}

                    python {score_file.absolute()} {task_output_file.absolute()} {task_score_file.absolute()}
                """))

    # Create a script that will submit all slurm jobs
    submit_all_sh = output_folder / "slurm-submit-all.sh"
    print(f"Creating {submit_all_sh.absolute()}")
    with open(submit_all_sh, "w") as f:
        for slurm in slurm_files:
            f.write(f"sbatch {slurm}\n")
    
    chmodx(submit_all_sh)

    rescore_all_sh = output_folder / "rescore-all.sh"
    print(f"Creating {rescore_all_sh.absolute()}")
    with open(rescore_all_sh, "w") as f:
        for folder in task_output_folders:
            f.write(f"python {score_file.absolute()} {folder.absolute()}\n")    

    chmodx(rescore_all_sh)
