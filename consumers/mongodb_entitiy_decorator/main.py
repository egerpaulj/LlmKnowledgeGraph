
import logging
from prometheus_client import Gauge, start_http_server
import threading
import os
import psutil

from llm_ner_nel.logging.logging_service import init_logging
from mongodb_entity_extractor import MongoDBConsumer

init_logging(app_name='llm_mongo_db_entity_decorator')

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

if __name__ == "__main__":
    
    consumer = MongoDBConsumer(
        database="Crawler",
        collection="crawler_responses_cleaned"
        
    )
    start_http_server(7777)
    logging.info("Prometheus metrics exposed on port 7777.")
    
    t = threading.Thread(target=monitor_resources, daemon=True)
    t.start()
    
    consumer.extract_entities()