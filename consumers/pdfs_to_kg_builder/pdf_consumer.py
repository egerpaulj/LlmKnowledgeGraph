from llm_ner_nel.inference_api.relationship_inference import RelationshipInferenceProvider, display_relationships
from llm_ner_nel.knowledge_graph.graph import KnowledgeGraph 
import logging
from pathlib import Path
from PyPDF2 import PdfReader
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

class PdfConsumer:
    def __init__(self, 
                 ollama_host, ollama_model, 
                 mlflow_host, mlflow_system_prompt_id, mlflow_user_prompt_id):
        self.relationships_extractor = RelationshipInferenceProvider(
            model=ollama_model,  
            ollama_host=ollama_host, 
            mlflow_tracking_host=mlflow_host, 
            mlflow_system_prompt_id = mlflow_system_prompt_id, 
            mlflow_user_prompt_id = mlflow_user_prompt_id)
        
        self.graph=KnowledgeGraph()
        
    def start(self, folder_path: str):
        folder = Path(folder_path)
        if not folder.exists():
            logging.error("Folder does not exist: %s", folder_path)
            return
        for file in folder.iterdir():
            if not file.is_file():
                continue
            if file.suffix.lower() != '.pdf':
                logging.info("Skipping non-pdf file: %s", file.name)
                continue
            try:
                reader = PdfReader(str(file))
                logging.info(f"reading file: {file.name}")
                for idx, page in enumerate(reader.pages, start=1):
                    try:
                        text = page.extract_text() or ""
                        logging.info(text)
                    except Exception as e:
                        logging.warning("Failed to extract text from %s page %d: %s", file.name, idx, e)
                        text = ""
                    title = ""
                    snippet = ""
                    logging.info(f"Processing: {file.name} - page {idx}")
                    if text:
                        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
                        for ln in lines[:6]:
                            if re.search(r'chapter\s+\d+', ln, re.I):
                                title = ln
                                break
                            if re.search(r'^\s*title[:\-\s]', ln, re.I):
                                title = ln
                                break
                            if ln.isupper() and 3 <= len(ln) <= 200 and len(ln.split()) <= 12:
                                title = ln
                                break
                            if ln.istitle() and len(ln.split()) <= 10:
                                title = ln
                                break
                        snippet = (lines[0] if lines else "")[:50]
                        
                        logging.info(f"Get relationships")
                        relationships = self.relationships_extractor.get_relationships(text=text)
                        display_relationships(relationships, True)
                        relationships.topic = title if title else snippet
                        
                        logging.info(f"Merge relationships")
                        self.graph.add_or_merge_relationships(result=relationships, src=file.name, src_type="pdf")
            except Exception as e:
                logging.error("Failed to read %s: %s", file.name, e)