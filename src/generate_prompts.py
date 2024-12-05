from common import VERSIONS, STRATEGIES, LANGUAGES, SPLITS
import random
from pathlib import Path
from preprocess_scan import parse_scan_line
from typing import List, Tuple
import json
import os

def partition(xs, predicate):
    yeses = []
    nos = []
    for x in xs:
        if predicate(x):
            yeses.append(x)
        else:
            nos.append(x)
    return (yeses, nos)

def is_output_equal(scan_line, out):
    _, output = parse_scan_line(scan_line)
    return output.strip() == out

def sample_train(train, n, special_handling):
    if special_handling == "add_prim_jump":
        # The "IN: jump OUT: I_JUMP" is repeated multiple times in the train set.
        without_prim = [ex for ex in train if not is_output_equal(ex, "I_JUMP")]
        prim = next(filter(lambda ex: is_output_equal(ex, "I_JUMP"), train))
        
        # Build context of n-1 examples without I_JUMP, and "primitive" example.
        context = random.sample(without_prim, n - 1)
        context.append(prim)

        # Shuffle it, so that the I_JUMP is introduced in a random location
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

def generate_prompt(
        strategy: str,
        context: List[Tuple[str , str]], # list of (q, a)
        test_question: str):
    
    if strategy == "basic":
        context_lines = [f"<s> IN: {question} OUT: {answer} </s>" for (question, answer) in context]
        final = f"<s> IN: {test_question} OUT: "
        return "\n".join(context_lines) + "\n" + final
    
    elif strategy == "instruction-1":
        # From https://aclanthology.org/2022.blackboxnlp-1.22.pdf
        return (
            f"<s> Here are some examples of converting complicated commands to correct navigation actions." + 
            f"\n\n" +
            f"\n\n".join([f"Command: {question}\nActions: {answer}" for (question, answer) in context]) +
            f"\n\n" +
            f"Command: {test_question}\n" +
            f"Actions: "
        )
    
    elif strategy == "instruction-2":
        # Variant of instruction-1, but different first sentence
        return (
            f"<s> Here are some examples of converting natural language commands to a list of machine actions." + 
            f"\n\n" +
            f"\n\n".join([f"Command: {question}\nActions: {answer}" for (question, answer) in context]) +
            f"\n\n" +
            f"Command: {test_question}\n" +
            f"Actions: "
        )
    
    elif strategy == "instruction-3":
        # Variant of instruction-1, but adding a more specific prompt asking to solve the problem
        return (
            f"<s> Here are some examples of converting complicated commands to correct navigation actions." + 
            f"\n\n" +
            f"\n\n".join([f"Command: {question}\nActions: {answer}" for (question, answer) in context]) +
            f"\n\n" +
            f"Please convert the following command into a list of machine actions:" +
            f"\n\n"
            f"Command: {test_question}\n" +
            f"Actions: "
        )
    
    elif strategy == "chain-of-thought":
        return (
            f"<s> Here are some examples of converting complicated commands to correct navigation actions." + 
            f"\n\n" +
            f"\n\n".join([f"Command: {question}\nActions: {answer}" for (question, answer) in context]) +
            f"\n\n" +
            f"Please convert the following command into a list of machine actions. Think step by step." +
            f"\n\n" +
            f"Command: {test_question}\n" +
            f"Actions: "
        )

    else:
        raise Exception(f"Strategy {strategy} is not implemented")


def generate_prompts(
        train_file: Path,
        test_file: Path,
        strategy: str,
        special_handling: str,
        context_size: int, # number of exemplars per prompt
        num_prompts: int,  # number of total prompts
        seed: int):

    random.seed(seed)
    
    with open(train_file, "r") as f:
        train = f.read().splitlines()

    with open(test_file, "r") as f:
        test = f.read().splitlines()

    # List of test questions we will ask the model
    test_samples = random.sample(test, num_prompts)

    prompts = []
    for test_sample in test_samples:
        # Sample context from training test
        exemplars = sample_train(train, context_size, special_handling)

        # Parse
        (question, answer) = parse_scan_line(test_sample)
        exemplars_parsed = [parse_scan_line(x) for x in exemplars]

        # Generate prompt from context + test question
        prompt = generate_prompt(
            strategy=strategy,
            context=exemplars_parsed,
            test_question=question)
        
        prompts.append({
            "prompt": prompt,
            "expected_answer": answer
        })

    return prompts

def generate_prompts_json(
        train_file: Path,
        test_file: Path,
        strategy: str,
        special_handling: str,
        context_size: int, # number of exemplars per prompt
        num_prompts: int,  # number of total prompts
        seed: int,
        output_file: Path):
    
    os.makedirs(output_file.parent, exist_ok=True)

    prompts = generate_prompts(
        train_file = train_file,
        test_file = test_file,
        strategy = strategy,
        special_handling = special_handling,
        context_size = context_size,
        num_prompts = num_prompts, 
        seed = seed)
    
    with open(output_file, "w") as f:
        json.dump(prompts, f)


def generate_all_prompts_json():
    

    for lang in LANGUAGES:
        for split in SPLITS:
            for strategy in STRATEGIES:
                for version_name, params in VERSIONS.items():

                    special_handling = None
                    if split == "add_prim_jump" or split == "add_prim_turn_left":
                        special_handling = split

                    print(f"Generating version {lang} {split} {strategy} {version_name}")

                    generate_prompts_json(
                        train_file = Path("data/output/datasets") / lang / split / "train.txt",
                        test_file = Path("data/output/datasets") / lang / split / "test.txt",
                        strategy = strategy,
                        special_handling = special_handling,
                        context_size = params["context_size"],
                        num_prompts = params["num_prompts"],
                        seed = params["seed"],
                        output_file = Path("data/output/prompts") / lang / split / strategy / version_name / "prompts.json"
                    )

if __name__ == "__main__":
    generate_all_prompts_json()