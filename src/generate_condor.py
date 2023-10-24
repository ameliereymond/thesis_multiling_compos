import os
from pathlib import Path
from textwrap import dedent
import os
import stat

models = ["xglm", "llama"]
# splits = ["mcd1", "mcd2", "mcd3", "add_prim_jump", "add_prim_turn_left", "length_split", "simple"]
splits = ["simple", "mcd1", "length_split"]
langs = ["en", "fr", "cmn", "hin", "ru"]

cmds = []
for model in models:
    output_folder = Path("scripts") / "generated" / model
    os.makedirs(output_folder.absolute(), exist_ok=True)

    for lang in langs:
        for split in splits:
            bash_file = output_folder / f"run-{model}-{lang}-{split}.sh"
            cmd_file = output_folder / f"run-{model}-{lang}-{split}.cmd"
            cmds.append(cmd_file)

            with open(bash_file, "w") as f:
                special_handling = ""
                if split == "add_prim_jump" or split == "add_prim_turn_left":
                    special_handling = f"--special-handling {split}"
                
                f.write("#!/bin/bash\n")
                f.write(dedent(f"""
                    conda init bash
                    conda activate mscan2

                    python ./src/experiment_{model}.py \\
                        --train data/output/{lang}/{split}/train.txt \\
                        --test data/output/{lang}/{split}/test.txt \\
                        --output data/output/results/{model}/{lang}/{split}/results.json \\
                        {special_handling} > run-{model}-{lang}-{split}.out
                """))
            
            with open(cmd_file, "w") as f:
                f.write(dedent(f"""
                    executable = {bash_file}
                    getenv     = true
                    error      = run-{model}-{lang}-{split}.error
                    log        = run-{model}-{lang}-{split}.log
                    notification = complete
                    transfer_executable = false
                    request_GPUs = 1
                    queue
                """))

submit_all_sh = output_folder / "condor-submit-all.sh"
with open(submit_all_sh, "w") as f:
    for cmd in cmds:
        f.write(f"condor_submit {cmd}\n")

st = os.stat(submit_all_sh).st_mode
os.chmod(submit_all_sh, st | stat.S_IEXEC)
