import os
from typing import Type
from openai import OpenAI
from llm_ner_nel.inference_api.llm_config import LlmConfig
from llm_ner_nel.inference_api.strategies.base import T, LLMProviderStrategy

class OpenAIStrategy(LLMProviderStrategy):
    def __init__(self, llm_config: LlmConfig):
        key = os.environ.get("OPENAI_API_KEY")
        
        # can use the OpenAi API client for other providers (e.g. Grok)
        base_url = os.environ.get("OPENAI_API_BASE_URL")
        
        if not key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        if base_url:
            self.client = OpenAI(api_key=key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=key)
            
        self.llm_config = llm_config

    def inference(self, prompt: str, system: str, model: str, json_response_type: Type[T]) -> T:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system", 
                    "content": system
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        
        content = response.choices[0].message.content
        
        if content is None:
            raise ValueError("OpenAI API returned empty content")
        
        return json_response_type.model_validate_json(content)