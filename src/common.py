VERSIONS = {
    "v1": {
        "num_prompts": 100,
        "context_size": 5,
        "seed": 1,
    },
    "v2": {
        "num_prompts": 100,
        "context_size": 10,
        "seed": 1,
    },
}

STRATEGIES = ["basic", "instruction-1", "instruction-2", "instruction-3", "chain-of-thought"]
LANGUAGES = ["cmn", "en", "fr", "hin", "ru"]
SPLITS = ["add_prim_jump", "add_prim_turn_left", "length_split", "mcd1", "mcd2", "mcd3", "simple"]

MODELS = {
    "aya": { "gpu_count": 2 },
    "bloom": { "gpu_count": 2 },
    "bloomz": { "gpu_count": 1 },
    "bloomz-mt": { "gpu_count": 1 },
    "llama-3-8B": { "gpu_count": 1 },
    "llama-3-8B-instruct": { "gpu_count": 1 },
    "xglm": { "gpu_count": 1 }
}
