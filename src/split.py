import sys
import json
import os
from pathlib import Path
import numpy as np

def write_scan(output_file, lines):
    with open(output_file, 'w') as f:
        for line in lines:
            f.write(line + "\n")

def split(input_file, output_folder, split_file):
    output_folder = Path(output_folder)
    os.makedirs(output_folder.absolute(), exist_ok=True)

    with open(input_file, 'r') as f:
        text = f.read().splitlines()

    with open(split_file, 'r') as f:
        indices_data = json.load(f)
        
    text_array = np.array(text)
    train = text_array[indices_data["trainIdxs"]]
    test = text_array[indices_data["testIdxs"]]
    dev = text_array[indices_data["devIdxs"]]

    write_scan(output_folder / "train.txt", train)
    write_scan(output_folder / "test.txt", test)
    write_scan(output_folder / "dev.txt", dev)

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_folder = sys.argv[2]
    split_file = sys.argv[3]

    split(input_file, output_folder, split_file)

