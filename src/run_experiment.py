from model import Model, XGLMLocalModel, AyaLocalModel, BloomLocalModel, BloomzLocalModel, LlamaLocalModel
from transformers import GenerationConfig
import argparse
from experiment import run_experiment, aggregate_scores, dump_logs
import os
from dotenv import load_dotenv

MODELS = ["aya", "bloomz", "bloomz-mt", "bloom", "xglm", "bloom", "llama-3-8B", "llama-3-8B-instruct"]

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

def get_hf_token():
    if "HF_TOKEN" not in os.environ:
        raise Exception("The HF_TOKEN environment variable should be set to a HuggingFace token")
    
    if not os.environ["HF_TOKEN"].startswith("hf_"):
        raise Exception("The HF_TOKEN environment variable is set, but was not recognized as a HuggingFace token (it should start with hf_)")
        
    return os.environ["HF_TOKEN"]


def get_model(args):
    config = GenerationConfig(max_new_tokens = args.max_output_length)

    if args.model == "aya":
        return AyaLocalModel("CohereForAI/aya-101", config)
    elif args.model == "bloom":
        return BloomLocalModel("bigscience/bloom-7b1", config)
    elif args.model == "bloomz":
        # Note: bloomz, not bloom!
        return BloomzLocalModel("bigscience/bloomz-7b1", config)
    elif args.model == "bloomz-mt":
        # Note: bloomz-mt, not bloomz!
        return BloomzLocalModel("bigscience/bloomz-7b1-mt", config)
    elif args.model == "xglm":
        return XGLMLocalModel("facebook/xglm-7.5B", config)
    elif args.model == "llama-3-8B":
        return LlamaLocalModel("meta-llama/Meta-Llama-3-8B", hf_auth_token=get_hf_token(), generation_config=config)
    elif args.model == "llama-3-8B-instruct":
        return LlamaLocalModel("meta-llama/Meta-Llama-3-8B-Instruct", hf_auth_token=get_hf_token(), generation_config=config)
    else:
        raise Exception(f"Model {args.model} is not implemented")


if __name__ == "__main__":
    load_dotenv()
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
