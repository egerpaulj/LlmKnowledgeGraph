from llm_ner_nel.inference_api.relationship_inference import RelationshipInferenceProvider, display_relationships
from llm_ner_nel.knowledge_graph.graph import KnowledgeGraph 
import logging
from pathlib import Path
from strategies.pdf_strategy import PdfProcessorStrategy
from strategies.epub_strategy import EpubProcessorStrategy

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

class DocumentConsumer:
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
        self.strategies = {
            '.pdf': PdfProcessorStrategy(),
            '.epub': EpubProcessorStrategy()
        }
        
    def start(self, folder_path: str):
        folder = Path(folder_path)
        if not folder.exists():
            logging.error("Folder does not exist: %s", folder_path)
            return
        for file in folder.iterdir():
            if not file.is_file():
                continue
            
            strategy = self.strategies.get(file.suffix.lower())
            if not strategy:
                logging.warning("Skipping unsupported file: %s", file.name)
                continue
            
            try:
                for document_page in strategy.process(str(file)):
                    title = document_page.title
                    text = document_page.text
                    logging.info(f"Processing: {file.name} - {title}")
                    
                    if text:
                        logging.info(text)
                        logging.info(f"Merging relationships")
                        
                        relationships = self.relationships_extractor.get_relationships(text=text)
                        relationships.topic = title
                        
                        display_relationships(relationships=relationships, console_log=True)
                        self.graph.add_or_merge_relationships(result=relationships, src=f"{file.name}-{title}", src_type=file.suffix.lower()[1:])
            except Exception as e:
                logging.error("Failed to read %s: %s", file.name, e)