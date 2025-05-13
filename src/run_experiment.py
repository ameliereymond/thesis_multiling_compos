from model import Model, XGLMLocalModel, AyaLocalModel, BloomLocalModel, BloomzLocalModel, LlamaLocalModel, OpenAIChatCompletionModel, RetryStrategy
from transformers import GenerationConfig
import argparse
from experiment import run_experiment, aggregate_scores, dump_logs
import os
from dotenv import load_dotenv
from common import MODELS


def parse_args():
    parser = argparse.ArgumentParser(description='Run an inference experiment')
    parser.add_argument("--prompts-file", help="Path to a json file containing prompts and expected answers", required=True, type=str)
    parser.add_argument("--model", help="Name of the model", required=True, choices=MODELS.keys())
    parser.add_argument("--max-output-length", help="Max number of output tokens", required=False, default=150, type=int)
    parser.add_argument("--output", help="Output file", required=True)
    return parser.parse_args()

def get_hf_token():
    if "HF_TOKEN" not in os.environ:
        raise Exception("The HF_TOKEN environment variable should be set to a HuggingFace token")
    
    if not os.environ["HF_TOKEN"].startswith("hf_"):
        raise Exception("The HF_TOKEN environment variable is set, but was not recognized as a HuggingFace token (it should start with hf_)")
        
    return os.environ["HF_TOKEN"]

def get_openai_token():
    if "OPENAI_API_KEY" not in os.environ:
        raise Exception("The OPENAI_API_KEY environment variable should be set to an OpenAI API key")
    
    if not os.environ["OPENAI_API_KEY"].startswith("sk-"):
        raise Exception("The OPENAI_API_KEY environment variable is set, but was not recognized as a OpenAI API token (it should start with sk-)")

    return os.environ["OPENAI_API_KEY"]

def get_model(args):
    config = GenerationConfig(max_new_tokens = args.max_output_length)

    if args.model == "aya":
        return AyaLocalModel(
            "CohereForAI/aya-101",
            config,
            chat_template=False
        )
    elif args.model == "aya-expanse-8b":
        return AyaLocalModel(
            "CohereLabs/aya-expanse-8b",
            config,
            chat_template=True
        )
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
        return LlamaLocalModel(
            "meta-llama/Meta-Llama-3-8B",
            hf_auth_token=get_hf_token(),
            generation_config=config,
            chat_template=False
        )
    elif args.model == "llama-3-8B-instruct":
        return LlamaLocalModel(
            "meta-llama/Meta-Llama-3-8B-Instruct",
            hf_auth_token=get_hf_token(),
            generation_config=config,
            chat_template=True
        )
    elif args.model in set(["o4-mini-2025-04-16"]):
        return OpenAIChatCompletionModel(
            model_name=args.model,
            api_key=get_openai_token(),
            retry_strategy=RetryStrategy(
                max_retries=20,
                initial_backoff=3, # Sleep for 3 seconds on first failure
                backoff_factor=1.5, # Sleep 50% longer on each additional failure
                max_backoff=60
            ),
            max_completion_tokens=16384 # openai default
        )
    else:
        raise Exception(f"Model {args.model} is not implemented")


if __name__ == "__main__":
    load_dotenv()
    args = parse_args()
    model = get_model(args)

    logs = run_experiment(
        model,
        prompts_file = args.prompts_file)
    
    print(aggregate_scores(logs))
    dump_logs(logs, args.output)
