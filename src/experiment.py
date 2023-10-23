import os
from model import Model
import random
import json
from pathlib import Path
import nltk
import time
from preprocess_scan import parse_scan_line

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

def is_output_equal(scan_line, out):
    _, output = parse_scan_line(scan_line)
    return output.strip() == out

def sample_train(train, n, special_handling):
    if special_handling == "add_prim_jump":
        without_prim = [ex for ex in train if not is_output_equal(ex, "I_JUMP")]
        prim = next(filter(lambda ex: is_output_equal(ex, "I_JUMP"), train))
        context = random.sample(without_prim, n - 1)
        context.append(prim)
        random.shuffle(context)
        return context
    elif special_handling == "add_prim_turn_left":
        without_prim = [ex for ex in train if not is_output_equal(ex, "I_TURN_LEFT")]
        prim = next(filter(lambda ex: is_output_equal(ex, "I_TURN_LEFT"), train))
        context = random.sample(without_prim, n - 1)
        context.append(prim)
        random.shuffle(context)
        return context
    else:
        return random.sample(train, n)

def build_queries(train, test, num_queries, context_size, special_handling = None):    
    tests = random.sample(test, num_queries)
    queries = []
    for test_sample in tests:
        (question, answer) = parse_scan_line(test_sample)
        question = markup_question(question)
        answer = markup_answer(answer)
        
        exemplars = sample_train(train, context_size, special_handling)
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
    
    return {
        "number_samples": len(logs),
        "sum_exact_matches": exact_matches,
        "avg_edit_distance": avg_edit_distance,
        "avg_expected_length": avg_expected_length,
        "edit_distances": [score["edit_distance"] for score in scores]
    }

##############
# EXPERIMENT #
##############

def run_experiment(model: Model,
                   train_file: str,
                   test_file: str,
                   num_queries: int,
                   context_size: int,
                   special_handling: str = None,
                   sleep_between_queries: float = 0):
    
    with open(train_file, "r") as f:
        train = f.read().splitlines()

    with open(test_file, "r") as f:
        test = f.read().splitlines()

    logs = []
    queries = build_queries(train,
                            test,
                            num_queries=num_queries,
                            context_size=context_size,
                            special_handling=special_handling)
    
    for i, (prompt, expected) in enumerate(queries):
        print(f"Testing example {i + 1} / {num_queries}")
        actual = model.infer(prompt)

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

        # Sleep between each query to avoid getting rate limited.
        # Don't sleep if this is the last query.
        if sleep_between_queries and i < len(queries) - 1:
            time.sleep(sleep_between_queries)
    
    return logs

def dump_logs(logs, output_file):
    os.makedirs(Path(output_file).parent.absolute(), exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(logs, f)
