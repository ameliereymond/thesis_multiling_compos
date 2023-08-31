import json
import os
from pathlib import Path

def get_line_indices(file, source_indices):    
    with open(file, 'r') as f:
        lines = f.read().splitlines()
    
    return [source_indices[line] for line in lines]

def create_split_file(source_file, train_file, dev_file, test_file, out_file):
    with open(source_file, 'r') as f:
        source = f.read().splitlines()
    
    source_dict = {line: i for i, line in enumerate(source)}

    train_idxs = get_line_indices(train_file, source_dict) if train_file else []
    dev_idxs = get_line_indices(dev_file, source_dict) if dev_file else []
    test_idxs = get_line_indices(test_file, source_dict) if test_file else []

    if (len(train_idxs) + len(dev_idxs) + len(test_idxs)) != len(source_dict):
        print("WARNING! The train + dev + test splits don't have the same number of elements as the source!")
        print(f"  train + dev + test have length {len(train_idxs) + len(dev_idxs) + len(test_idxs)}")
        print(f"  source has length {len(source_dict)}")
    
    if len(set(train_idxs)) != len(train_idxs):
        print(f"WARNING! There are {len(train_idxs) - len(set(train_idxs))} repeated items in train (there should be 0)")

    if len(set(dev_idxs)) != len(dev_idxs):
        print(f"WARNING! There are {len(dev_idxs) - len(set(dev_idxs))} repeated items in dev (there should be 0)")

    if len(set(test_idxs)) != len(test_idxs):
        print(f"WARNING! There are {len(test_idxs) - len(set(test_idxs))} repeated items in test (there should be 0)")

    intersection = set.intersection(set(train_idxs), set(dev_idxs), set(test_idxs))
    if len(intersection) > 0:
        print(f"WARNING! There are {len(intersection)} items in the intersection of test, dev, train (there should be 0)")

    os.makedirs(Path(out_file).parent.absolute(), exist_ok=True)

    with open(out_file, 'w') as f:
        f.write(json.dumps({
            "trainIdxs": train_idxs,
            "devIdxs": dev_idxs,
            "testIdxs": test_idxs,
        }))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Create a JSON split file from already split files')
    
    parser.add_argument("--source", help="Source file, containing all lines", required=True)
    parser.add_argument("--train", help="File containing train set lines")
    parser.add_argument("--dev", help="File containing dev set lines")
    parser.add_argument("--test", help="File containing test set lines")
    parser.add_argument("--output", help="Output file", required=True)
    
    args = parser.parse_args()

    create_split_file(args.source, args.train, args.dev, args.test, args.output)
