from llm_ner_nel.inference_api.llm_config import LlmConfig
from llm_ner_nel.inference_api.strategies.base import LLMProviderStrategy
from llm_ner_nel.inference_api.strategies.google_ai_studio import GoogleStrategy
from llm_ner_nel.inference_api.strategies.google_ai_studio_slim import GoogleSlimStrategy
from llm_ner_nel.inference_api.strategies.ollama import OllamaStrategy
from llm_ner_nel.inference_api.strategies.ollama_slim import OllamaSlimStrategy
from llm_ner_nel.inference_api.strategies.openai import OpenAIStrategy
from llm_ner_nel.inference_api.strategies.gpt_oss import GptOssStrategy
from llm_ner_nel.inference_api.strategies.openai_slim import OpenAISlimStrategy


def create_inference_strategy_local(name: str, llm_config: LlmConfig, ollama_host = "http://localhost:11434") -> LLMProviderStrategy:
    local_ollama_host = ollama_host
    if name=="google":
        return GoogleStrategy()
    if name=="google-slim":
        return GoogleSlimStrategy()
    if name=="openai":
        return OpenAIStrategy(llm_config=llm_config)
    if name=="openai-slim":
        return OpenAISlimStrategy(llm_config=llm_config)
    if name == "gpt-oss":
        return GptOssStrategy(llm_config=llm_config)
    if name == "ollama-slim":
        return OllamaSlimStrategy(host=local_ollama_host, llm_config=llm_config)
    
    return OllamaStrategy(host=local_ollama_host, llm_config=llm_config)