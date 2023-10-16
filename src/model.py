from abc import ABC, abstractmethod
from huggingface_hub import InferenceApi
import time
from transformers import AutoTokenizer, XGLMModel, XGLMConfig

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
                 max_output_length: int = 20,
                 top_k: int = 50):
        '''
        model_name: HuggingFace pretrained XGLM model name, e.g., facebook/xglm-564M
        
        max_output_length: Maximum length that will be used by default in the generate method of the model.

        top_k:      Number of highest probability vocabulary tokens to keep for top-k-filtering
                    that will be used by default in the generate method of the model.
        '''
        self.model_name = model_name
        self.model = XGLMModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def infer(self, prompt: str) -> str:
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        output = self.model.generate(
            input_ids,
            max_length=50,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            top_k=50)
        
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text