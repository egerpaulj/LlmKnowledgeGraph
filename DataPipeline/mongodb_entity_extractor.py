import threading
from pymongo import MongoClient
from prometheus_client import Counter, Summary, Gauge, start_http_server
import logging
import os
import psutil
from LlmKnowledgeGraph.InferenceApi.entityInference import EntityInferenceProvider, display_entities, get_unique_entity_names

logging.basicConfig(
    level=logging.INFO,  # Set the minimum log level
    format='%(asctime)s - %(levelname)s - %(message)s',
)

MESSAGE_COUNT = Counter('messages_processed_total_mongodb', 'Total number of messages processed')
MESSAGE_FAIL_COUNT = Counter('messages_processed_total_mongodb_failed', 'Total number of messages processed')
MESSAGE_PROCESSING_TIME = Summary('message_processing_seconds_mongodb', 'Time spent processing a message')
CPU_USAGE = Gauge('process_cpu_percent_mongodb', 'Process CPU usage percent')
MEMORY_USAGE = Gauge('process_memory_mb_mongodb', 'Process memory usage in MB')

def monitor_resources():
            process = psutil.Process(os.getpid())
            while True:
                try:
                    cpu = process.cpu_percent(interval=1)
                    mem = process.memory_info().rss / (1024 * 1024)  # MB
                    CPU_USAGE.set(cpu)
                    MEMORY_USAGE.set(mem)
                except Exception as e:
                    logging.error(f"Error updating resource metrics: {e}")
                import time
                time.sleep(5)
                
class MongoDBConsumer:
    def __init__(self, database: str, collection: str):
        self.client = MongoClient(os.getenv('MONGODB_CONNECTION_STRING', "mongodb://localhost:27017"))
        self.db = self.client[database]
        self.collection = self.db[collection]
        self.batch_size = 100
        
        ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2')
        mlflow_tracking_host = os.getenv('MLFLOW_TRACKING_HOST', 'http://localhost:5050')
        mlflow_system_prompt_id = os.getenv('MLFLOW_SYSTEM_PROMPT_ID', None)
        mlflow_user_prompt_id = os.getenv('MLFLOW_USER_PROMPT_ID', None)
        
        self.entity_extractor = EntityInferenceProvider(
            model=ollama_model, 
            ollama_host=ollama_host, 
            mlflow_tracking_host=mlflow_tracking_host, 
            mlflow_system_prompt_id=mlflow_system_prompt_id,
            mlflow_user_prompt_id=mlflow_user_prompt_id)
        
        self.logger = logging.getLogger(__name__)

    def extract_entities(self):
        try:
            query = {"entities": None}
            
            # Get total count for logging purposes
            total_docs = self.collection.count_documents(query)
            self.logger.info(f"Found {total_docs} documents to process")

            processed = 0
            while True:
                # Get batch of documents
                cursor = self.collection.find(query).limit(self.batch_size)
                batch = list(cursor)
                
                if not batch:
                    break

                # Process each document in the batch
                for doc in batch:
                    MESSAGE_COUNT.inc()
                    with MESSAGE_PROCESSING_TIME.time():
                        try:
                            text = doc["text"]
                            uri = doc["src"]
                            id=doc["_id"]
                            
                            self.logger.info(f"Processing: {uri}, with text: {text}, id:{id}")
                            entities = self.entity_extractor.get_entities(text=text)
                            
                            display_entities(entities=entities)
                            unique_entity_names = get_unique_entity_names(entities=entities)
                            
                            self.logger.info(f"Adding entities to mongodb: {uri}")
                            
                            self.collection.update_one(
                                {"_id": id},
                                {"$set": {"entities": unique_entity_names}}
                            )
                            
                            processed += 1
                            
                            if processed % 100 == 0:
                                self.logger.info(f"Processed {processed}/{total_docs} documents")
                                
                        except Exception as e:
                            MESSAGE_FAIL_COUNT.inc()
                            self.logger.error(f"Error processing document {doc['_id']}. Uri: {uri}: {str(e)}")
                            continue

            self.logger.info(f"Completed processing {processed} documents")
            
        except Exception as e:
            self.logger.error(f"Error in batch processing: {str(e)}")
        finally:
            self.client.close()
            



if __name__ == "__main__":
    consumer = MongoDBConsumer(
        database="Crawler",
        collection="crawler_responses_cleaned"
        
    )
    start_http_server(7777)
    logging.info("Prometheus metrics exposed on port 7777.")
    
    # Monitor CPU and memory usage in the background
    t = threading.Thread(target=monitor_resources, daemon=True)
    t.start()
    
    consumer.extract_entities()
