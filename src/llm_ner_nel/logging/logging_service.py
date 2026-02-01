import logging

from llm_ner_nel.logging.elasticsearch_handler import create_elastic_search_handler
def create_console_handler():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    return console_handler

def init_logging(app_name: str):
    logging.basicConfig(
        level=logging.INFO,  
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[create_elastic_search_handler(app_name=app_name), create_console_handler()])