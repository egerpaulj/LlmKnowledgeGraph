# import sys
# import os

# sys.path.append(os.path.abspath("../src"))

# from llm_ner_nel.inference_api.entity_inference import EntityInferenceProvider, display_entities


# text = '''Vincent de Groof is a Dutch-born Belgian early pioneering aeronaut. He created an early model of an ornithopter'''
# inference_provider = EntityInferenceProvider(model="qwen3.5:9b", strategy="ollama", ollama_hos="http://ollama:11434") 
# entities = inference_provider.get_entities(text)
# display_entities(entities, console_log=True)



import logging
from typing import Type
from llm_ner_nel.core.dto import Entities
from llm_ner_nel.inference_api.llm_config import LlmConfig
from ollama import Client

client = Client(host="http://localhost:11434")

response = client.generate(
            prompt="""
            
You are an expert in named entity recognition. Your task is to perform  named entity recognition on text and identify entities.

# Rules

## Entity Name
- Always use the full name of the entity. Attempt to deduce the full name based on the context.  For example, use "Barack Obama" instead of just "Obama" or "Barack".
- Do not use the sentence as the entity name. Instead map the sentence to a relevant entity.
- Limit the number of words in the entity to 5. It should not be a sentence nor phrase.
- If the name is obvious, then use the full name of the individual.
- Json response only, skip all other output

Below are a number of examples of text and their extracted entities. Entities should have the full name. 

## Focus
Focus on extracting entities.

## Example
Input: "In 2022, Tesla partnered with Panasonic to expand its battery production at the Gigafactory in Nevada. Elon Musk said the collaboration would accelerate the development of next-generation cells.",

Result:
{   
    entities : [       
            {
                "name":"Tesla",
                "type":"Organization",
                "confidence":1.0,
            },
            {
                "name":"Panasonic",
                "type":"Organization",
                "confidence":1.0,
            },
            {
                "name":"Gigafactory Nevada",
                "type":"Facility/Location",
                "confidence":1.0,
            },
            {
                "name":"Elon Musk",
                "type":"Person",
                "confidence":1.0,
            },
            {
                "name":"Next-generation cells",
                "type":"Product/Technology",
                "confidence":1.0,
            }
        ]
    }
}

Extract entities from text using named entity recognition. 

Extract this: 

Vincent de Groof is a Dutch-born Belgian early pioneering aeronaut. He created an early model of an ornithopter
            
            """,
            model="qwen3.5:9b"
        )

print(response.response)
json = Entities.model_validate_json(response.response)
print(json)
        