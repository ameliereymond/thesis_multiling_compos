from model import LlamaLocalModel
from transformers import GenerationConfig
from experiment import run_experiment, aggregate_scores, dump_logs

model = LlamaLocalModel("meta-llama/Llama-2-7b-chat-hf", GenerationConfig(max_new_tokens = 150))

logs = run_experiment(
    model,
    "../data/output/en/simple/train.txt",
    "../data/output/en/simple/test.txt",
    num_queries=10,
    context_size=10,
    special_handling=None,
    sleep_between_queries=None)

print(aggregate_scores(logs))
dump_logs(logs, "output-tmp.txt")