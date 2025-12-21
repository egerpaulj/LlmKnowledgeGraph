import os
from pyexpat import model
from google import genai
from typing import Optional, Type
from llm_ner_nel.inference_api.strategies.base import T, LLMProviderStrategy
from google.genai.types import GenerateContentConfig, HttpOptions
from google.genai import types


class GoogleStrategy(LLMProviderStrategy):
    def __init__(self, api_key: Optional[str] = None):
        
        key = api_key or os.environ.get("GEMINI_API_KEY")
        if not key:
             raise ValueError("Missing GEMINI_API_KEY environment variable")
        self.client = genai.Client(api_key=key, http_options=HttpOptions(api_version="v1"))
        self.cache = None


    def inference(self, prompt: str, system: str, model: str, json_response_type: Type[T]) -> T:
        if self.cache == None:
            self.cache = self.client.caches.create(
                model=model,
                config=types.CreateCachedContentConfig(
                    display_name='ner', 
                    system_instruction=(system),
                    ttl="300s"
                )
            )
            
        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(cached_content=self.cache.name))
        
        
        return json_response_type.model_validate_json(response.text)
        