from model import Model, XGLMLocalModel, AyaLocalModel, BloomzLocalModel
from transformers import GenerationConfig
import argparse
from experiment import run_experiment, aggregate_scores, dump_logs

MODELS = ["aya", "bloomz", "bloomz-mt", "bloom", "xglm"]

def parse_args():
    parser = argparse.ArgumentParser(description='Run an inference experiment')
    parser.add_argument("--model", help="Name of the model", required=True, choices=MODELS)
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
    return parser.parse_args()


def get_model(args):
    if args.model == "aya":
        return AyaLocalModel("CohereForAI/aya-101", GenerationConfig(max_new_tokens = args.max_output_length))
    elif args.model == "bloomz":
        return BloomzLocalModel("bigscience/bloomz-7b1", GenerationConfig(max_new_tokens = args.max_output_length))
    elif args.model == "bloomz-mt":
        return BloomzLocalModel("bigscience/bloomz-7b1-mt", GenerationConfig(max_new_tokens = args.max_output_length))
    elif args.model == "bloom":
        raise Exception("bloom not supported yet")
    elif args.model == "xglm":
        return XGLMLocalModel("facebook/xglm-7.5B", GenerationConfig(max_new_tokens = args.max_output_length))
    else:
        raise Exception(f"Model {args.model} is not implemented")


if __name__ == "__main__":
    args = parse_args()
    model = get_model(args)

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