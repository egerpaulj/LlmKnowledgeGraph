"""
Usage (example):
python main.py --path-to-dir /mnt/pdfs
"""
import argparse
from document_consumer import DocumentConsumer

import sys
import logging
import os

logging.basicConfig(
    level=logging.INFO,  # Set the minimum log level
    format='%(asctime)s - %(levelname)s - %(message)s',
)
def _parse_args():
    p = argparse.ArgumentParser(description="Consume pdfs, extract entities and relationships and merge to a knowledge graph")
    p.add_argument("--path-to-dir", required=True, help="Path to the pdf folders.")
    return p.parse_args()
    
if __name__ == '__main__':
    ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2')
    ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2')
    mlflow_tracking_host = os.getenv('MLFLOW_TRACKING_HOST', 'http://localhost:5050')
    mlflow_system_prompt_id = os.getenv('MLFLOW_SYSTEM_PROMPT_ID', None)
    mlflow_user_prompt_id = os.getenv('MLFLOW_USER_PROMPT_ID', None)
        

    consumer = DocumentConsumer(
        ollama_host=ollama_host,
        ollama_model=ollama_model,
        mlflow_host=mlflow_tracking_host,
        mlflow_system_prompt_id=mlflow_system_prompt_id,
        mlflow_user_prompt_id=mlflow_user_prompt_id
    )
    args = _parse_args()
    try:
        consumer.start(folder_path=args.path_to_dir)
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)
