default_entity_recognition_system_prompt = """
TOOOODOOOOO get exmaples from mlflow backup
  """
  
default_knowledge_graph_system_prompt = """
TOOOODOOOOO get exmaples from mlflow backup
  """
  
def default_entity_recognition_user_prompt(text: str) -> str:
    return f"""
TOOOODOOOOO get exmaples from mlflow backup
Extract this: {text}"""


def default_knowledge_graph_user_prompt(text: str) -> str:
    return f"""
TOOOODOOO get from mlflow backup
Extract this: {text}"""