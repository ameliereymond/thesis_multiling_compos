import os
from huggingface_hub import InferenceApi
import random
import json
from pathlib import Path
import nltk
import time
from preprocess_scan import parse_scan_line

random.seed(0)

#############
# INFERENCE #
#############

API_TOKEN = os.environ["HF_TOKEN"]
inference = InferenceApi("bigscience/bloom",token=API_TOKEN)

def infer(prompt,
         max_length = 32,
         seed = 42,
         retry_count: int = 15,
         retry_delay_seconds: float = 2,
         retry_exponential_backoff: float = 1.5,
         retry_max_delay_seconds: float = 30):

    params = {
        "max_new_tokens": max_length,
        "do_sample": False,
        "seed": seed,
        "return_full_text": False,
        "eos_token_id": 2
    }

    return do_infer(
        prompt=prompt,
        params=params,
        retry_count=retry_count,
        retry_delay_seconds=retry_delay_seconds,
        retry_exponential_backoff=retry_exponential_backoff,
        retry_max_delay_seconds=retry_max_delay_seconds)

def do_infer(
        prompt,
        params,
        retry_count: int,
        retry_delay_seconds: float,
        retry_exponential_backoff: float,
        retry_max_delay_seconds: float):
    
    if retry_count <= 0:
        raise Exception("Ran out of retries")
    
    result = inference(prompt, params=params)
    print(result)
    
    if isinstance(result, dict) and "error" in result.keys():
        error = result["error"]
        print(f"Got an error: '{error}'. Will sleep {retry_delay_seconds} seconds, then retry. {retry_count - 1} attempts left")
        
        time.sleep(retry_delay_seconds)

        new_delay = min(retry_max_delay_seconds, retry_delay_seconds ** retry_exponential_backoff)

        return do_infer(
            prompt,
            params,
            retry_count = retry_count - 1,
            retry_delay_seconds = new_delay,
            retry_exponential_backoff = retry_exponential_backoff,
            retry_max_delay_seconds = retry_max_delay_seconds)

    return result[0]["generated_text"]

#############
# DATA LOAD #
#############

def markup_example(scan_line):
    (question, answer) = parse_scan_line(scan_line)
    return markup_question(question) + markup_answer(answer)

def markup_question(question):
    return f"<s>IN: {question} OUT: "

def markup_answer(answer):
    return answer + "</s>"

def build_queries(train, test, num_queries, context_size):    
    tests = random.sample(test, num_queries)
    queries = []
    for test_sample in tests:
        (question, answer) = parse_scan_line(test_sample)
        question = markup_question(question)
        answer = markup_answer(answer)
        
        exemplars = random.sample(train, context_size)
        exemplars = [markup_example(ex) for ex in exemplars]
        context = "\n\n".join(exemplars)
        
        prompt = context + "\n\n" + question 
        queries.append((prompt, answer))
    
    return queries

###########
# SCORING #
###########

def compute_exact_match_score(expected, actual):
    expected = expected.strip().split(" ")
    actual = actual.strip().split(" ")
    
    # If the actual string wasn't able to stop by itself,
    # cut it at the expected length.
    if len(actual) > len(expected):
        actual = actual[:len(expected)]
    
    return 1 if actual == expected else 0
    
def compute_edit_distance_score(expected, actual):
    expected = expected.strip().removesuffix("</s>").split(" ")
    actual = actual.strip().removesuffix("</s>").split(" ")
    
    # If the actual string wasn't able to stop by itself,
    # cut it at the expected length.
    if len(actual) > len(expected):
        actual = actual[:len(expected)]
        
    return nltk.edit_distance(actual, expected)

def compute_normalized_edit_distance_score(expected, actual):
    expected = expected.strip().removesuffix("</s>").split(" ")
    actual = actual.strip().removesuffix("</s>").split(" ")
    
    # If the actual string wasn't able to stop by itself,
    # cut it at the expected length.
    if len(actual) > len(expected):
        actual = actual[:len(expected)]
        
    return nltk.edit_distance(actual, expected) / len(expected)
    
def compute_scores(expected, actual):
    return {
        "exact_match": compute_exact_match_score(expected, actual),
        "edit_distance": compute_edit_distance_score(expected, actual),
        "normalized_edit_distance": compute_normalized_edit_distance_score(expected, actual)
    }

def avg(lst):
    return sum(lst) / len(lst)

def num_instructions(answer):
    return len(answer.strip().removesuffix("</s>").split(" "))

def aggregate_scores(logs):
    scores = [log["scores"] for log in logs]
    exact_matches = sum([score["exact_match"] for score in scores])
    avg_edit_distance = avg([score["edit_distance"] for score in scores])
    avg_expected_length = avg([num_instructions(log["expected"]) for log in logs])
    print(f"Avg edit distance: {avg_edit_distance} / {avg_expected_length}")

##############
# EXPERIMENT #
##############

def run_experiment(train, test, num_queries, context_size, max_length=150):
    logs = []
    queries = build_queries(train, test, num_queries=num_queries, context_size=context_size)

    for i, (prompt, expected) in enumerate(queries):
        print(f"Testing example {i + 1} / {num_queries}")
        print(prompt)
        actual = infer(prompt, max_length=max_length)

        scores = compute_scores(expected, actual)
        
        print(f"Got:      {actual}")
        print()
        print(f"Expected: {expected}")
        print()
        print(scores)
        print()
        
        log = {
            "prompt": prompt,
            "expected": expected,
            "actual": actual,
            "scores": scores
        }
        
        logs.append(log)
    
    return logs

def dump_logs(logs, output_file):
    os.makedirs(Path(output_file).parent.absolute(), exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(logs, f)

def main(
        train_file: str,
        test_file: str,
        output_file: str,
        num_queries: int = 100,
        context_size: int = 10,
        max_length: int = 150
):
    with open(train_file, "r") as f:
        train = f.read().splitlines()

    with open(test_file, "r") as f:
        test = f.read().splitlines()

    logs = run_experiment(
        train,
        test,
        num_queries=num_queries,
        context_size=context_size,
        max_length=max_length)
    
    aggregate_scores(logs)
    dump_logs(logs, output_file)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Run an inference experiment on BLOOM')
    
    parser.add_argument("--train", help="File containing train set lines", required=True)
    parser.add_argument("--test", help="File containing test set lines", required=True)
    parser.add_argument("--output", help="Output file", required=True)
    parser.add_argument("--context-size", help="Number of exemplars in the context", default=10, type=int)

    args = parser.parse_args()

    main(
        train_file = args.train,
        test_file = args.test,
        output_file = args.output,
        context_size = args.context_size
    )