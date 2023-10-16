import sys
import json
import os
from pathlib import Path
from inference import aggregate_scores

if __name__ == "__main__":
    logs_file = sys.argv[1]
    output_file = sys.argv[2]

    print(f"Rescoring {logs_file} -> {output_file}")

    with open(logs_file, 'r') as f:
        logs = json.load(f)

    scores = aggregate_scores(logs)

    os.makedirs(Path(output_file).parent.absolute(), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(scores, f, indent=4)
