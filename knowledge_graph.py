
from typing import List
from py2neo import Graph, Node, Relationship
from pydantic import BaseModel, Field
from ollama import Client

class NeoDbConfig:
    uri: str
    username: str
    password: str
    
    def __init__(self, **kwargs):
        self.uri = kwargs.get('uri', 'neo4j://localhost:7687')
        self.username = kwargs.get('username', "neo4j")
        self.password = kwargs.get('password', "password")
        
class LlmConfig:

    def __init__(self, **kwargs):
        # Set default values
        self.model = kwargs.get('model', 'llama3.2')
        self.temperature = kwargs.get('temperature', 0.0)
        self.top_k = kwargs.get('top_k', 1)
        self.top_p = kwargs.get('top_p', None)
        self.max_tokens = kwargs.get('max_tokens', 40)
        self.repeat_penalty = kwargs.get('repeat_penalty', None)
        self.frequency_penalty = kwargs.get('frequency_penalty', None)
        self.presence_penalty = kwargs.get('presence_penalty', None)
        self.typical_p = kwargs.get('typical_p', None)
        self.num_thread = kwargs.get('num_thread', None)
        
    model: str
    temperature: float
    top_k: int
    top_p: float
    max_tokens: int
    repeat_penalty: float
    frequency_penalty: float
    presence_penalty: float
    typical_p: float
    num_thread: int
    
def generate_clean_text_prompt(text: str) ->str:
    
    return f"""
        You are a sophisticated text editor. Your task is to rewrite the provided text, removing all pronouns and substituting each with the specific noun it refers to. Prioritize maintaining the original 
        meaning and sentence structure.  Consider the context to accurately determine the correct noun.  If the noun is ambiguous, choose the most logical option.

        Here's an example:

        Original Text: "John Jones bought some crickets. His bought items were amazing. John was happy"
        Rewritten Text: "John Jones bought some crickets. John Jones' bought crickets were amazing. John Jones was happy"

        Now, rewrite the following text:

        Text:
        [{text}]"""

class CleanText(BaseModel):
    original: str = Field(
        description="Original text"
        
    )
    converted: str = Field(
        description="Converted text"
    )
    
class NerNel(BaseModel):
    head: str = Field(
        description=(
            "extracted head entity like Microsoft, Apple, John. "
            "Must use human-readable unique identifier."
        )
    )
    head_type: str = Field(
        description="type of the extracted head entity like Person, Company, etc"
    )
    relation: str = Field(description="relation between the head and the tail entities")
    tail: str = Field(
        description=(
            "extracted tail entity like Microsoft, Apple, John. "
            "Must use human-readable unique identifier."
        )
    )
    tail_type: str = Field(
        description="type of the extracted tail entity like Person, Company, etc"
    )

class Relationships(BaseModel):
    relationships: List[NerNel]


system_prompt_1 = """
    "# Knowledge Graph Instructions for GPT-4\n"
    "## 1. Overview\n"
    "You are a top-tier algorithm designed for extracting information in structured "
    "formats to build a knowledge graph.\n"
    "Try to capture as much information from the text as possible without "
    "sacrificing accuracy. Do not add any information that is not explicitly "
    "mentioned in the text.\n"
    "- **Nodes** represent entities and concepts.\n"
    "- **Nodes** identify the pronoun to an entity and use the full name (no abbrevations).\n"
    "- The aim is to achieve simplicity and clarity in the knowledge graph, making it\n"
    "accessible for a vast audience.\n"
    "## 2. Labeling Nodes\n"
    "- **Consistency**: Ensure you use available types for node labels.\n"
    "Ensure you use basic or elementary types for node labels.\n"
    "- For example, when you identify an entity representing a person, "
    "always label it as **'person'**. Avoid using more specific terms "
    "like 'mathematician' or 'scientist'."
    "- **Node IDs**: Never utilize integers as node IDs. Node IDs should be "
    "names or human-readable identifiers found in the text.\n"
    "- **Relationships** represent connections between entities or concepts.\n"
    "Ensure consistency and generality in relationship types when constructing "
    "knowledge graphs. Instead of using specific and momentary types "
    "such as 'BECAME_PROFESSOR', use more general and timeless relationship types "
    "like 'PROFESSOR'. Make sure to use general and timeless relationship types!\n"
    "## 3. Coreference Resolution\n"
    "- **Maintain Entity Consistency**: When extracting entities, it's vital to "
    "ensure consistency.\n"
    'If an entity, such as "John Doe", is mentioned multiple times in the text '
    'but is referred to by different names or pronouns (e.g., "Joe", "he"),'
    "always use the most complete identifier for that entity throughout the "
    'knowledge graph. In this example, use "John Doe" as the entity ID.\n'
    "Remember, the knowledge graph should be coherent and easily understandable, "
    "so maintaining consistency in entity references is crucial.\n"
    "## 4. Strict Compliance\n"
    "Adhere to the rules strictly. Non-compliance will result in termination.'
    '## 5. Examples
    'Use the examples but don't include the examples in the output'
    ## 6 extract relationships similar to the list below from the sentences. Create new nodes and relationships when necessary:
**I. Family Relationships**

PARENT_OF
MARRIED_TO
SIBLING_OF
CHILD_OF
GRANDPARENT_OF
GRANDCHILD_OF
AUNT_OF
UNCLE_OF
COUSIN_OF
NIECE_OF
NEPHEW_OF
STEP_PARENT_OF
STEP_CHILD_OF
STEP_SIBLING_OF
ADOPTED_BY
RELATED_TO

**II. Professional Relationships**

WORKS_FOR
EMPLOYEE_OF
FOUNDER_OF
CEO_OF
BOARD_MEMBER_OF
PARTNER_OF (Business)
COLLEAGUE_OF
SUPERVISOR_OF
SUBORDINATE_OF
CLIENT_OF
ATTORNEY_OF
AGENT_OF
MANAGER_OF
COACH_OF
TEACHER_OF
STUDENT_OF
TRAINEE_OF
MENTOR_OF

**III. Political/Social Relationships**

GOVERNED_BY
LEADER_OF
MEMBER_OF (Party/Organization)
SUPPORTER_OF
OPPONENT_OF
ALLY_OF
ENEMY_OF
CITIZEN_OF
RESIDENT_OF
SUCCESSOR_OF
PREDECESSOR_OF
VOTED_FOR
ELECTED_BY
NOMINATED_BY
SPONSORED_BY
ADVISOR_TO
AMBASSADOR_TO
DIPLOMAT_TO

**IV. Geographic Relationships**

LOCATED_IN
PART_OF (e.g., "Paris, part of France")
NEAR
FOUNDED_IN
CAPTURED_BY
CONTROLLED_BY
BORDERING
ORIGINATED_IN
DIAGRAM_OF
MAP_OF
CLOSE_TO
INHABITED_BY

**V. Possessions/Associations**

OWNS
HAS_AWARD
HAS_TITLE
HAS_ROLE
PLAYS_ROLE_IN
HAS_HOBBY
HAS_MEMBERSHIP
HAS_WEBSITE
PUBLISHED_BY
AUTHORED_BY
DESIGNED_BY
PRODUCED_BY
BUILT_BY
FUNDED_BY
PATENTED_BY
ENDORSED_BY

**VI. Events/Time Relationships**

PARTICIPATED_IN
ATTENDED
SPEAKING_AT
PERFORMED_AT
DATE_OF
TIME_OF
CAUSE_OF
RESULT_OF
BEFORE
AFTER
DURING
SIMULTANEOUS_WITH
LEAD_TO
TRIGGERED_BY
FOLLOWED_BY
REPLACED_BY
INSPIRED_BY

**VII. Miscellaneous Relationships**

RESEMBLES
NAMED_AFTER
KNOWN_FOR
INFLUENCED_BY
DESCRIBED_AS
ASSOCIATED_WITH
CONNECTED_TO
REPresents (Symbolic)
SYMBOL_OF
FEATURED_IN
APPEARS_IN
COMPARISON_TO
TRANSLATED_BY
EDITED_BY
ILLUSTRATED_BY
COMMISSIONED_BY
SUPPORTED_BY (Financially)
DOCUMENTED_IN
REPORTED_BY
"""

        
examples = """{
        "example": (
            "Adam is a software engineer in Microsoft since 2009, "
            "and last year he got an award as the Best Talent"
        ),
        "head": "Adam",
        "head_type": "Person",
        "relation": "WORKS_FOR",
        "tail": "Microsoft",
        "tail_type": "Company",
    },
    {
        "example": (
            "Adam is a software engineer in Microsoft since 2009, "
            "and last year he got an award as the Best Talent"
        ),
        "head": "Adam",
        "head_type": "Person",
        "relation": "HAS_AWARD",
        "tail": "Best Talent",
        "tail_type": "Award",
    },
    {
        "example": (
            "Microsoft is a tech company that provide "
            "several products such as Microsoft Word"
        ),
        "head": "Microsoft Word",
        "head_type": "Product",
        "relation": "PRODUCED_BY",
        "tail": "Microsoft",
        "tail_type": "Company",
    },
    {
        "example": "Microsoft Word is a lightweight app that accessible offline",
        "head": "Microsoft Word",
        "head_type": "Product",
        "relation": "HAS_CHARACTERISTIC",
        "tail": "lightweight app",
        "tail_type": "Characteristic",
    },
    {
        "ecample": "Microsoft Word is a lightweight app that accessible offline",
        "head": "Microsoft Word",
        "head_type": "Product",
        "relation": "HAS_CHARACTERISTIC",
        "tail": "accessible offline",
        "tail_type": "Characteristic",
    },"""

class KnowledgeGraph:
    model: str
    llm_config: LlmConfig
    neo_config: NeoDbConfig
    
    client=Client(host='http://localhost:11434')
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
                    
    def create_graph_document(self, result: Relationships):
        nodes_set = set()

        for rel in result.relationships:
            if rel.head_type == None or rel.head == '':
                continue
            if rel.tail_type == None or rel.tail == '':
                continue
            
            head_node = (rel.head_type, rel.head)
            tail_node = (rel.tail_type, rel.tail)
            
            print(f'Node found: {rel.head}')
            print(f'Node found: {rel.tail}')

            nodes_set.add(head_node)
            nodes_set.add(tail_node)

        nodes = [Node(title, identity=identity, title=title) for identity, title in nodes_set]

        for node in nodes:
            self.graph.merge(node, node.get("title"), "title")

        for rel in result.relationships:
            if rel.head_type == None or rel.head == '':
                continue
            if rel.tail_type == None or rel.tail == '':
                continue
            print(f'Relationship found: {rel.relation}')
            
            head_node = self.get_node(nodes, rel.head)
            tail_node = self.get_node(nodes, rel.tail)

            self.graph.create(Relationship(
                    head_node,
                    rel.relation,
                    tail_node
                ))
    
    def add_to_graph(self, text: str):
        cleaned = text
        prompt = self.generate_prompt(cleaned, examples)
        
        result = self.inference(
            prompt=prompt, 
            system=system_prompt_1)
        
        self.create_graph_document(result)