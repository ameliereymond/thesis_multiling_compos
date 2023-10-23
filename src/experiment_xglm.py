from experiment import run_experiment, aggregate_scores, dump_logs
from model import XGLMLocalModel
from transformers import GenerationConfig

def main():
    model = XGLMLocalModel("facebook/xglm-564M", GenerationConfig(max_new_tokens = 150))
    
    logs = run_experiment(
        model,
        "data/output/en/simple/train.txt",
        "data/output/en/simple/test.txt",
        num_queries=10,
        context_size=5,
        special_handling=None,
        sleep_between_queries=None)
    
    print(aggregate_scores(logs))
    dump_logs(logs, "output-tmp.txt")


if __name__ == "__main__":
    main()