from cleanText import CleanText
from llmConfig import LlmConfig
from neoDbConfig import NeoDbConfig
from relationships import Relationships
from knowledge_graph import examples, generate_clean_text_prompt, system_prompt_1


from ollama import Client
from py2neo import Graph, Node, Relationship


import logging
from typing import List


class KnowledgeGraph:
    model: str
    ollama_host: str
    llm_config: LlmConfig
    neo_config: NeoDbConfig
    graph: Graph

    def __init__(self, **kwargs):
        self.model = kwargs.get('model', "llama3.2")
        self.llm_config = LlmConfig(model=self.model,
                       temperature = 0.5,
                       top_p = 0.3,
                       typical_p = 0.9,
                       top_k = 50,
                       max_tokens = 256,
                       repeat_penalty = 1.2,
                       frequency_penalty = 0.1,
                       presence_penalty = 0.1,
                       num_thread = 16
                       )
        self.neo_config = kwargs.get('neoDbConfig', NeoDbConfig())
        self.graph = Graph(self.neo_config.uri, auth=(self.neo_config.username, self.neo_config.password))
        self.ollama_host =  kwargs.get('ollama_host', "http://localhost:11434")
        self.client=Client(host=self.ollama_host)



    def inference(self, prompt: str, system: str) -> Relationships:
        options = {
            "top_k": self.llm_config.top_k,
            "top_p": self.llm_config.top_p,
            "max_tokens": self.llm_config.max_tokens,
            "temperature": self.llm_config.temperature,
            "repeat_penalty": self.llm_config.repeat_penalty,
            "frequency_penalty": self.llm_config.frequency_penalty,
            "typical_p": self.llm_config.typical_p,
            "num_thread": self.llm_config.num_thread,
        }
        logging.info(self.ollama_host)
        response = self.client.generate(
                                prompt=prompt,
                                system=system,
                                model=self.llm_config.model,
                                format=Relationships.model_json_schema(),
                                options = options)
        return Relationships.model_validate_json(response.response)

    def clean_text(self, text: str) -> CleanText:
        options = {
            "top_k": self.llm_config.top_k,
            "top_p": self.llm_config.top_p,
            "max_tokens": self.llm_config.max_tokens,
            "temperature": self.llm_config.temperature,
            "repeat_penalty": self.llm_config.repeat_penalty,
            "frequency_penalty": self.llm_config.frequency_penalty,
            "typical_p": self.llm_config.typical_p,
            "num_thread": self.llm_config.num_thread,
        }
        response = self.client.generate(
                                prompt=generate_clean_text_prompt(text),
                                system="Replace pronouns with the actual representation. Return a json only and skip the explanation.",
                                model=self.llm_config.model,
                                format=CleanText.model_json_schema(),
                                options = options)
        return CleanText.model_validate_json(response.response)

    def get_node(self, nodes: List[Node], title: str) -> Node:

        for node in nodes:
            if node.get("title") == title:
                return node
        return None

    def generate_prompt(self, text, examples):
        return f"""Based on the following example, extract entities and "
                    f"relations from the provided text.\n\n",
                    f"Your task is to extract relationships from text. The relationships can only appear "
                    f"between specific node types are presented in the schema format "
                    f"like: (Entity1Type, RELATIONSHIP_TYPE, Entity2Type) /n"
                    f"Below are a number of examples of text and their extracted "
                    f"entities and relationships."
                    f"Examples: {examples}\n\nExtract this: {text}"""

    def create_graph_document(self, result: Relationships, src: str, src_type: str):
        nodes_set = set()

        for rel in result.relationships:
            if rel.head_type == None or rel.head == '':
                continue
            if rel.tail_type == None or rel.tail == '':
                continue

            head_node = (rel.head_type, rel.head)
            tail_node = (rel.tail_type, rel.tail)

            logging.info(f'Node found: {rel.head}')
            logging.info(f'Node found: {rel.tail}')

            nodes_set.add(head_node)
            nodes_set.add(tail_node)

        nodes = [Node(title, identity=identity, title=title, src=src, src_type=src_type) for identity, title in nodes_set]

        for node in nodes:
            self.graph.merge(node, node.get("title"), "title")

        for rel in result.relationships:
            if rel.head_type == None or rel.head == '':
                continue
            if rel.tail_type == None or rel.tail == '':
                continue
            logging.info(f'Relationship found: {rel.relation}')

            head_node = self.get_node(nodes, rel.head)
            tail_node = self.get_node(nodes, rel.tail)

            self.graph.create(Relationship(
                    head_node,
                    rel.relation,
                    tail_node
                ))

    def add_to_graph(self, text: str, src: str, src_type: str):
        cleaned = text
        prompt = self.generate_prompt(cleaned, examples)

        result = self.inference(
            prompt=prompt,
            system=system_prompt_1)

        self.create_graph_document(result, src, src_type)