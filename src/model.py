from abc import ABC, abstractmethod
from huggingface_hub import InferenceApi
import time
import transformers
from transformers import AutoTokenizer, XGLMForCausalLM, GenerationConfig, LlamaTokenizer, LlamaForCausalLM
import torch

class Model(ABC):
    @abstractmethod
    def infer(self, prompt: str) -> str:
        pass

class RetryStrategy:
    def __init__(self,
                 max_retries: int,
                 initial_backoff: float,
                 backoff_factor: float,
                 max_backoff: float):
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff
        self.backoff_factor = backoff_factor
        self.max_backoff = max_backoff

    @staticmethod
    def none():
        return RetryStrategy(max_retries=0, initial_backoff=0, backoff_factor=1, max_backoff=None)

    def execute_with_retry(self, action):
        retries = 0
        while retries < self.max_retries:
            try:
                result = action()
                return result  # If the action is successful, return its result
            except Exception as e:
                print(f"Attempt {retries + 1} failed: {str(e)}")
                retries += 1
                if retries < self.max_retries:
                    backoff_time = self.get_backoff(retries)                    
                    print(f"Retrying in {backoff_time} seconds...")
                    time.sleep(backoff_time)
                else:
                    print("Max retries reached. Exiting.")
                    raise
    
    def get_backoff(self, retry_number):
        backoff_time = self.initial_backoff * (self.backoff_factor ** retry_number)
        if self.max_backoff is not None:
            return min(backoff_time, self.max_backoff)
        else:
            return backoff_time

class HuggingFaceInferenceApiModel(Model):
    def __init__(self,
                 model_name: str,
                 hf_token: str,
                 retry_strategy: RetryStrategy,
                 seed: int,
                 max_output_length: int,
                 eos_token_id: int):
        self.inference = InferenceApi(model_name, token = hf_token)
        self.params = {
            "max_new_tokens": max_output_length,
            "do_sample": False,
            "seed": seed,
            "return_full_text": False,
            "eos_token_id": eos_token_id
        }
        self.retry_strategy = retry_strategy
    
    def infer(self, prompt: str) -> str:
        return self.retry_strategy.execute_with_retry(lambda: self.infer_without_retry(prompt))
    
    def infer_without_retry(self, prompt: str) -> str:
        result = self.inference(prompt, params=self.params)
        if isinstance(result, dict) and "error" in result.keys():
            error = result["error"]
            raise Exception(f"Got an error: '{error}'. Prompt was: '{prompt}'")
        else:
            return result[0]["generated_text"]

class XGLMLocalModel(Model):
    def __init__(self,
                 model_name: str,
                 generation_config: GenerationConfig = GenerationConfig()):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = XGLMForCausalLM.from_pretrained(model_name).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        # See https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig
        self.generation_config = generation_config

    def infer(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            labels=inputs["input_ids"],
            generation_config=self.generation_config)

        return self.tokenizer.decode(outputs.tolist()[0], skip_special_tokens=False)

class LlamaLocalModel(Model):
    def __init__(self,
                 model_name: str,
                 generation_config: GenerationConfig = GenerationConfig()):
        
        # Create model
        self.model = LlamaForCausalLM.from_pretrained(model_name, use_auth_token="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")

        # Place model on all available GPUs, and otherwise on CPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        # Create tokenizer
        self.tokenizer = LlamaTokenizer.from_pretrained(model_name, use_auth_token="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")
        
        # Store generation config
        # See https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig
        self.generation_config = generation_config

    def infer(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            labels=inputs["input_ids"],
            generation_config=self.generation_config)

        return self.tokenizer.decode(outputs.tolist()[0], skip_special_tokens=False)