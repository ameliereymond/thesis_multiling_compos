import random
import os
from experiment import run_experiment, aggregate_scores, dump_logs
from model import HuggingFaceInferenceApiModel, RetryStrategy

def main(
        model_name: str,
        train_file: str,
        test_file: str,
        output_file: str,
        num_queries: int,
        context_size: int,
        max_output_length: int,
        special_handling: str, # optional
        random_seed: int
):
    random.seed(random_seed)

    model = HuggingFaceInferenceApiModel(
        model_name = model_name,
        hf_token = os.environ["HF_TOKEN"],
        retry_strategy = RetryStrategy(
            max_retries = 7,
            initial_backoff = 2,
            backoff_factor = 1.5,
            max_backoff = 900
        ),
        max_output_length = max_output_length,
        seed = 42,
        eos_token_id = 2
    )

    logs = run_experiment(
        model,
        train_file,
        test_file,
        num_queries=num_queries,
        context_size=context_size,
        special_handling=special_handling,
        sleep_between_queries = 2)
    
    print(aggregate_scores(logs))
    dump_logs(logs, output_file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Run an inference experiment on BLOOM')
    
    parser.add_argument("--model-name", help="Name of the Hugging Face model to use", required=False, default="bigscience/bloom", type=str)
    parser.add_argument("--train", help="File containing train set lines", required=True)
    parser.add_argument("--test", help="File containing test set lines", required=True)
    parser.add_argument("--output", help="Output file", required=True)
    parser.add_argument("--context-size", help="Number of exemplars in the context", required=False, default=8, type=int)
    parser.add_argument("--num-queries", help="The number of queries to try in the experiment", required=False, default=100, type=int)
    parser.add_argument("--random-seed", help="Seed for random.seed, used to randomize data selection", required=False, default=0, type=int)
    parser.add_argument("--max-output-length", help="Max number of output tokens", required=False, default=150, type=int)
    parser.add_argument("--special-handling",
                        help="Choose a type of special query building",
                        choices=["add_prim_turn_left", "add_prim_jump"],
                        required=False,
                        default=None)
    
    args = parser.parse_args()

    print("-------------- RUN EXPERIMENT --------------")
    print(args)
    print("--------------------------------------------")

    main(
        model_name = args.model_name,
        train_file = args.train,
        test_file = args.test,
        output_file = args.output,
        context_size = args.context_size,
        num_queries = args.num_queries,
        max_output_length = args.max_output_length,
        special_handling = args.special_handling,
        random_seed = args.random_seed
    )

    print("-------------- END EXPERIMENT --------------")

