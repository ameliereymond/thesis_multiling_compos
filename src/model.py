from abc import ABC, abstractmethod
from huggingface_hub import InferenceApi
import time
from transformers import AutoTokenizer, XGLMForCausalLM, GenerationConfig, LlamaTokenizer, LlamaForCausalLM, AutoModelForCausalLM
import torch
import requests

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
        self.model = self.model.to(self.device)

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

class BloomzLocalModel(Model):
    def __init__(self,
                 model_name: str,
                 generation_config: GenerationConfig = None):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)


        # See https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig

        if generation_config is None:
            self.generation_config = GenerationConfig(
                max_new_tokens=150,
                num_return_sequences=1,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=1.0
            )
        else:
            self.generation_config = generation_config

    def infer(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                labels=inputs["input_ids"],
                generation_config=self.generation_config
            )

        return self.tokenizer.decode(outputs.tolist()[0], skip_special_tokens=False)
        

class OpenAIModel(Model):
    def __init__(self, 
                 model_name: str,
                 api_key: str,
                 retry_strategy: RetryStrategy,
                 max_output_tokens: int):
        self.api_key = api_key
        self.model_name = model_name
        self.retry_strategy = retry_strategy

        completion_style_models = set([
            "babbage", "text-babbage-001", "davinci", "curie-instruct-beta", "davinci-instruct-beta",
            "text-davinci-001", "babbage-002", "davinci-002", "text-davinci-002", "fanw-json-eval",
            "gpt-3.5-turbo-instruct-0914", "ada", "text-ada-001", "gpt-3.5-turbo-instruct",
            "text-davinci-003", "text-curie-001", "curie"
        ])
        
        chat_completion_style_models = set([
            "gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-0314",
            "gpt-3.5-turbo-0613", "gpt-3.5-turbo-0301", "gpt-4-0613"
        ])
        
        if model_name in chat_completion_style_models:
            self.use_chat_completion = True
        elif model_name in completion_style_models:
            self.use_chat_completion = False
            if max_output_tokens > 20:
                raise Exception("Are you sure you want such a high max_output_tokens? " +
                                "This might be expensive. Comment out this exception if you're really certain")
        else:
            raise Exception(f"Model name '{model_name}' not recognized")
        
        self.max_output_tokens = max_output_tokens

    def infer(self, prompt: str) -> str:
        return self.retry_strategy.execute_with_retry(lambda: self.infer_without_retry(prompt))

    def infer_without_retry(self, prompt: str) -> str:
        if self.use_chat_completion:
            return self.infer_chat_completion_style(prompt)
        else:
            return self.infer_completion_style(prompt)

    def infer_chat_completion_style(self, prompt: str) -> str:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            json = {
                "model": self.model_name,
                # The OpenAI default is inf, which is expensive!
                "max_tokens": self.max_output_tokens,
                "messages": [

                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        if response.status_code == 200:
            try:
                json = response.json()
                return json["choices"][0]["message"]["content"]
            except Exception as e:
                print(e)
                print(response.text)
                raise Exception("Error parsing response")
        else:
            raise Exception(f"OpenAI returned HTTP {response.status_code} with message {response.json()}")
        

    def infer_completion_style(self, prompt: str) -> str:
        response = requests.post(
            "https://api.openai.com/v1/completions",
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            json = {
                "model": self.model_name,
                # The OpenAI default is 16, which is low!
                # BUT these models tend to be expensive...
                "max_tokens": self.max_output_tokens,
                "prompt": prompt
            }
        )

        if response.status_code == 200:
            try:
                json = response.json()
                return json["choices"][0]["text"]
            except Exception as e:
                print(e)
                print(response.text)
                raise Exception("Error parsing response")
        else:
            raise Exception(f"OpenAI returned HTTP {response.status_code} with message {response.json()}")

