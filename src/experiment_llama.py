from model import LlamaLocalModel
from transformers import GenerationConfig
from experiment import run_experiment, aggregate_scores, dump_logs
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run an inference experiment on BLOOM')
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

    model = LlamaLocalModel("meta-llama/Llama-2-7b-chat-hf", GenerationConfig(max_new_tokens = args.max_output_length))

    logs = run_experiment(
        model,
        train_file = args.train,
        test_file = args.test,
        num_queries = args.num_queries,
        context_size = args.context_size,
        special_handling = args.special_handling,
        sleep_between_queries = None)

    print(aggregate_scores(logs))
    dump_logs(logs, args.output)