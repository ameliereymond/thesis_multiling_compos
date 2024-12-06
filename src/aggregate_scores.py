import os
from pathlib import Path
import json
import csv
from common import MODELS, LANGUAGES, SPLITS, STRATEGIES, VERSIONS

models = ["aya", "bloomz", "bloomz-mt", "bloom", "xglm", "bloom"] # "llama-3-8B", "llama-3-8B-instruct"]
splits = ["mcd1", "mcd2", "mcd3", "add_prim_jump", "add_prim_turn_left", "length_split", "simple"]
langs = ["en", "fr", "cmn", "hin", "ru"]

def get_scores():
    for model in MODELS.keys():
        for lang in LANGUAGES:
            for split in SPLITS:
                for strategy in STRATEGIES:
                    for version in VERSIONS.keys():
                        results_path = Path("data") / "output" / "results" / model / lang / split / strategy / version / "score.json"
                        if results_path.exists():
                            with open(results_path, 'r') as f:
                                data = json.load(f)
                                yield {
                                    "model": model,
                                    "lang": lang,
                                    "split": split,
                                    "number_samples": data["number_samples"],
                                    "sum_exact_matches": data["sum_exact_matches"],
                                    "sum_exact_prefixes": data["sum_exact_prefixes"],
                                    "avg_edit_distance": data["avg_edit_distance"],
                                    "avg_expected_length": data["avg_expected_length"]
                                }
                        else:
                            print(f"Skipping {results_path} as it does not exist")

def write_aggregated_results(output_file: Path):
    with open(output_file, "w") as f:
        header_written = False
        for score in get_scores():
            w = csv.DictWriter(f, score.keys())
            if not header_written:
                w.writeheader()
                header_written = True
            w.writerow(score)

    print(f"Wrote aggregated results in {output_file.absolute()}")

write_aggregated_results(Path("data") / "output" / "results" / "aggregated_scores.csv")
