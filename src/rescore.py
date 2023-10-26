import sys
import json
import os
from pathlib import Path
from experiment import aggregate_scores

def rescore_results_file(results_file: Path, score_file: Path):
    with open(results_file, 'r') as f:
        results = json.load(f)

    scores = aggregate_scores(results)

    os.makedirs(Path(score_file).parent.absolute(), exist_ok=True)

    with open(score_file, 'w') as f:
        json.dump(scores, f, indent=4)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rescore.py [folder]")
        print("Converts all results.json files in the folder to score.json")
        sys.exit(1)

    logs_folder = sys.argv[1]

    for results_file in Path(logs_folder).rglob('results.json'):
        results_file = results_file.absolute()
        score_file = results_file.parent / "score.json"
        cwd = Path(os.getcwd()).absolute()
        print(f"Rescoring {results_file.relative_to(cwd)} -> {score_file.relative_to(cwd)}")
        rescore_results_file(results_file, score_file)