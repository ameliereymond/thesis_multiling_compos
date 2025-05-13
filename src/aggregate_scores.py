import os
from pathlib import Path
import json
import csv
import numpy as np
from common import MODELS, LANGUAGES, SPLITS, STRATEGIES, VERSIONS

models = ["aya", "bloomz", "bloomz-mt", "bloom", "xglm", "bloom", "llama-3-8B", "llama-3-8B-instruct", "o4-mini-2025-04-16"]
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
                                    "strategy": strategy,
                                    "version": version,
                                    "number_samples": data["number_samples"],
                                    "sum_exact_matches": data["sum_exact_matches"],
                                    "sum_exact_prefixes": data["sum_exact_prefixes"],
                                    "avg_expected_length": data["avg_expected_length"],

                                    # Edit distance
                                    "avg_edit_distance": data["avg_edit_distance"],
                                    "edit_distance_q1": np.percentile(data["edit_distances"], 25),
                                    "edit_distance_q2": np.percentile(data["edit_distances"], 50),
                                    "edit_distance_q3": np.percentile(data["edit_distances"], 75),
                                    
                                    # BLEU
                                    "avg_bleu": data["avg_bleu"],
                                    "bleu_q1": np.percentile(data["bleu_scores"], 25),
                                    "bleu_q2": np.percentile(data["bleu_scores"], 50),
                                    "bleu_q3": np.percentile(data["bleu_scores"], 75),

                                    # ROUGE1
                                    "avg_rouge1": data["avg_rouge1"],
                                    "rouge1_q1": np.percentile(data["rouge1_scores"], 25),
                                    "rouge1_q2": np.percentile(data["rouge1_scores"], 50),
                                    "rouge1_q3": np.percentile(data["rouge1_scores"], 75),

                                    # ROUGE2
                                    "avg_rouge2": data["avg_rouge2"],
                                    "rouge2_q1": np.percentile(data["rouge2_scores"], 25),
                                    "rouge2_q2": np.percentile(data["rouge2_scores"], 50),
                                    "rouge2_q3": np.percentile(data["rouge2_scores"], 75),

                                    # ROUGEL
                                    "avg_rougeL": data["avg_rougeL"],
                                    "rougeL_q1": np.percentile(data["rougeL_scores"], 25),
                                    "rougeL_q2": np.percentile(data["rougeL_scores"], 50),
                                    "rougeL_q3": np.percentile(data["rougeL_scores"], 75),

                                    # "avg_ter": data["avg_ter"],
                                }
                        else:
                            print(f"Skipping {results_path} as it does not exist")

def get_statistics():
    for model in MODELS.keys():
        for lang in LANGUAGES:
            scores = {
                "edit_distances": [],
                "bleu": [],
                "rouge1": [],
                "rouge2": [],
                "rougeL": []
            }

            for split in SPLITS:
                for strategy in STRATEGIES:
                    for version in VERSIONS.keys():
                        results_path = Path("data") / "output" / "results" / model / lang / split / strategy / version / "score.json"
                        if results_path.exists():
                            with open(results_path, 'r') as f:
                                data = json.load(f)
                                scores["edit_distances"].append(data["edit_distances"])
                                scores["bleu"].append(data["bleu_scores"])
                                scores["rouge1"].append(data["rouge1_scores"])
                                scores["rouge2"].append(data["rouge2_scores"])
                                scores["rougeL"].append(data["rougeL_scores"])
                        else:
                            print(f"Skipping {results_path} as it does not exist")
            
            yield {
                "model": model,
                "lang": lang,
                # BLEU
                "avg_bleu": np.average(scores["bleu"]),
                "bleu_q1": np.percentile(scores["bleu"], 25),
                "bleu_q2": np.percentile(scores["bleu"], 50),
                "bleu_q3": np.percentile(scores["bleu"], 75),

                # ROUGE1
                "avg_rouge1": np.average(scores["rouge1"]),
                "rouge1_q1": np.percentile(scores["rouge1"], 25),
                "rouge1_q2": np.percentile(scores["rouge1"], 50),
                "rouge1_q3": np.percentile(scores["rouge1"], 75),

                # ROUGE2
                "avg_rouge2": np.average(scores["rouge2"]),
                "rouge2_q1": np.percentile(scores["rouge2"], 25),
                "rouge2_q2": np.percentile(scores["rouge2"], 50),
                "rouge2_q3": np.percentile(scores["rouge2"], 75),

                # ROUGEL
                "avg_rougeL": np.average(scores["rougeL"]),
                "rougeL_q1": np.percentile(scores["rougeL"], 25),
                "rougeL_q2": np.percentile(scores["rougeL"], 50),
                "rougeL_q3": np.percentile(scores["rougeL"], 75),
            }

def write_csv(lines, output_file: Path):
    with open(output_file, "w") as f:
        header_written = False
        for line in lines:
            # Write header if this is the first
            w = csv.DictWriter(f, line.keys())
            if not header_written:
                w.writeheader()
                header_written = True
            
            # Write row
            w.writerow(line)

    print(f"Wrote {output_file.absolute()}")    

if __name__ == "__main__":
    folder = Path("data") / "output" / "results"

    write_csv(get_scores(), folder / "aggregated_scores_with_openai.csv")
    write_csv(get_statistics(), folder / "statistics_with_openai.csv")
