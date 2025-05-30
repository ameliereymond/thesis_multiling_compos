import os
from model import Model
import random
import json
from pathlib import Path
import nltk
import time
from preprocess_scan import parse_scan_line
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer 
import sacrebleu

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
        context = "\n".join(exemplars)
        
        prompt = context + "\n" + question 
        queries.append((prompt, answer))
    
    return queries

###########
# SCORING #
###########

def compute_exact_match_score(expected, actual):
    expected = expected.strip().removesuffix("</s>").split(" ")
    actual = actual.strip().removesuffix("</s>").split(" ")

    return 1 if actual == expected else 0

def compute_exact_prefix_score(expected, actual):
    expected = expected.strip().removesuffix("</s>").split(" ")
    actual = actual.strip().removesuffix("</s>").split(" ")
    
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

def compute_bleu_score(expected, actual):
    smoothing = SmoothingFunction()
    expected = [expected.strip().removesuffix("</s>").split(" ")] 
    actual = actual.strip().removesuffix("</s>").split(" ")  
    return sacrebleu.sentence_bleu(expected, actual, smoothing_function=smoothing.method1)

# def compute_ter_score(expected, actual):
#     expected = expected.strip().removesuffix("</s>").strip()
#     actual = actual.strip().removesuffix("</s>").strip()
#     return sacrebleu.sentence_ter(actual, [expected]).score


# Initialize ROUGE scorer
rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True) 

from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import sacrebleu

# Initialize ROUGE scorer
rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

# Compute BLEU Score
def compute_bleu_score(expected, actual):
    smoothing = SmoothingFunction()
    expected = [expected.strip().removesuffix("</s>").split(" ")]  # Reference as list of tokens
    actual = actual.strip().removesuffix("</s>").split(" ")  # Hypothesis as tokens
    return sentence_bleu(expected, actual, smoothing_function=smoothing.method1)

# Compute ROUGE Scores
def compute_rouge_scores(expected, actual):
    expected = expected.strip().removesuffix("</s>")
    actual = actual.strip().removesuffix("</s>")
    scores = rouge.score(expected, actual)
    return {
        "rouge1": scores['rouge1'].fmeasure,
        "rouge2": scores['rouge2'].fmeasure,
        "rougeL": scores['rougeL'].fmeasure,
    }


def compute_scores(expected, actual):
    return {
        "exact_match": compute_exact_match_score(expected, actual),
        "exact_prefix": compute_exact_prefix_score(expected, actual),
        "edit_distance": compute_edit_distance_score(expected, actual),
        "normalized_edit_distance": compute_normalized_edit_distance_score(expected, actual),
        "nltk_bleu": compute_bleu_score(expected, actual),
        #"ter": compute_ter_score(expected, actual),
        **compute_rouge_scores(expected, actual),
    }

def avg(lst):
    return sum(lst) / len(lst)

def num_instructions(answer):
    return len(answer.strip().removesuffix("</s>").split(" "))

def aggregate_scores(logs):
    scores = [compute_scores(expected=log["expected"], actual=log["actual"]) for log in logs]
    
    exact_matches = sum([score["exact_match"] for score in scores])
    exact_prefixes = sum([score["exact_prefix"] for score in scores])
    avg_edit_distance = avg([score["edit_distance"] for score in scores])
    avg_expected_length = avg([num_instructions(log["expected"]) for log in logs])
    avg_bleu = avg([score["nltk_bleu"] for score in scores])
    avg_rouge1 = avg([score["rouge1"] for score in scores])
    avg_rouge2 = avg([score["rouge2"] for score in scores])
    avg_rougeL = avg([score["rougeL"] for score in scores])
    #avg_ter = avg([score["ter"] for score in scores])

    return {
        "number_samples": len(logs),
        "sum_exact_matches": exact_matches,
        "sum_exact_prefixes": exact_prefixes,
        "avg_edit_distance": avg_edit_distance,
        "avg_expected_length": avg_expected_length,
        "avg_bleu": avg_bleu, 
        "avg_rouge1": avg_rouge1, 
        "avg_rouge2": avg_rouge2, 
        "avg_rougeL": avg_rougeL, 
        #"avg_ter": avg_ter,
        "edit_distances": [score["edit_distance"] for score in scores],        
        "bleu_scores": [score["nltk_bleu"] for score in scores],
        #"ter_scores": [score["ter"] for score in scores],
        "rouge1_scores": [score["rouge1"] for score in scores],
        "rouge2_scores": [score["rouge2"] for score in scores],
        "rougeL_scores": [score["rougeL"] for score in scores],
    }

##############
# EXPERIMENT #
##############

def run_experiment(model: Model,
                   prompts_file: Path,
                   sleep_between_queries: float = 0):
    
    with open(prompts_file, "r") as f:
        prompts = json.load(f)
    
    logs = []
    
    for i, item in enumerate(prompts):
        print(f"Testing example {i + 1} / {len(prompts)}")

        prompt = item["prompt"]
        expected = item["expected_answer"]

        actual = model.infer(prompt)
        
        print(f"Prompt:   {prompt}")
        print(f"Got:      {actual}")
        print(f"Expected: {expected}")
        
        scores = compute_scores(expected, actual)
        print()
        print(scores)
        print(flush=True)
        
        log = {
            "prompt": prompt,
            "expected": expected,
            "actual": actual,
            "scores": scores
        }
        
        logs.append(log)

        # Sleep between each query to avoid getting rate limited.
        # Don't sleep if this is the last query.
        if sleep_between_queries and i < len(prompts) - 1:
            time.sleep(sleep_between_queries)
    
    return logs

def dump_logs(logs, output_file):
    os.makedirs(Path(output_file).parent.absolute(), exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(logs, f)
