"""
Usage (example):
python main.py --path-to-dir /mnt/pdfs
"""
import argparse
from document_consumer import DocumentConsumer

import sys
import logging
import os
from llm_ner_nel.logging.logging_service import  init_logging

init_logging(app_name='llm_knowledge_graph_builder')

def _parse_args():
    p = argparse.ArgumentParser(description="Consume pdfs, extract entities and relationships and merge to a knowledge graph")
    p.add_argument("--path-to-dir", required=True, help="Path to the pdf folders.")
    return p.parse_args()
    
if __name__ == '__main__':
    
    ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2')
    mlflow_tracking_host = os.getenv('MLFLOW_TRACKING_HOST', 'http://localhost:5050')
    mlflow_system_prompt_id = os.getenv('MLFLOW_SYSTEM_PROMPT_ID', None)
    mlflow_user_prompt_id = os.getenv('MLFLOW_USER_PROMPT_ID', None)
    
    logging.info("Starting PDF to KG Builder")
    logging.info(f"Ollama Host: {ollama_host}, Model: {ollama_model}")
    logging.info(f"MLflow Host: {mlflow_tracking_host}")

    consumer = DocumentConsumer(
        ollama_host=ollama_host,
        ollama_model=ollama_model,
        mlflow_host=mlflow_tracking_host,
        mlflow_system_prompt_id=mlflow_system_prompt_id,
        mlflow_user_prompt_id=mlflow_user_prompt_id
    )
    args = _parse_args()
    try:
        logging.info(f"Processing documents from: {args.path_to_dir}")
        consumer.start(folder_path=args.path_to_dir)
        logging.info("PDF to KG processing completed successfully")
    except Exception as e:
        logging.error(f"Fatal error", e)
        sys.exit(1)
