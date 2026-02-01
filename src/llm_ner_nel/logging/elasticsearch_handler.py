"""Custom Elasticsearch logging handler for structured logging"""
import logging
import os
import sys
from datetime import datetime, timezone
from elasticsearch import Elasticsearch
from llm_ner_nel.logging.es_index_config import create_index_if_not_exists, setup_ilm_policy
import traceback

# Disable elasticsearch internal logging to prevent recursion
logging.getLogger('elasticsearch').setLevel(logging.CRITICAL)
logging.getLogger('elastic_transport').setLevel(logging.CRITICAL)


class ElasticsearchLoggingHandler(logging.Handler):
    """Custom logging handler that sends logs directly to Elasticsearch index"""

    def __init__(self, es_client: Elasticsearch, index_name, app_name='app', buffer_size=5):
        """
        Initialize Elasticsearch handler

        Args:
            hosts: List of Elasticsearch hosts. Can be:
                   - [{'scheme': 'http', 'host': 'localhost', 'port': 9200}]
                   - [{'host': 'localhost', 'port': 9200}] (scheme defaults to 'http')
                   - ['http://localhost:9200'] (string format)
            index_name: Base name for Elasticsearch index (will be appended with date)
            app_name: Application name for log context
            buffer_size: Number of logs to buffer before flushing
        """

        self.es = es_client
        self.index_name = index_name
        self.app_name = app_name
        self.buffer = []
        self.buffer_size = buffer_size
        
        super().__init__()

    def emit(self, record):
        """Emit a log record to Elasticsearch"""
        try:
            # Create structured log document
            log_doc = self._format_log_record(record)
            self.buffer.append(log_doc)

            # Flush buffer if it reaches the specified size
            if len(self.buffer) >= self.buffer_size:
                self.flush()

        except Exception:
            self.handleError(record)

    def _format_log_record(self, record):
        """Format a log record into a structured document"""
        timestamp = datetime.now(timezone.utc).replace(microsecond=0)

        try:
            message = record.getMessage()
        except Exception:
            message = record.msg

        doc = {
            '@timestamp': timestamp.isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': message,
            'app_name': self.app_name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            doc['exception'] = ''.join(traceback.format_exception(*record.exc_info))

        # Add extra fields from the record
        if hasattr(record, '__dict__'):
            for key, value in record.__dict__.items():
                if key not in ['name', 'msg', 'args', 'created', 'filename', 'funcName',
                              'levelname', 'levelno', 'lineno', 'module', 'msecs', 'message',
                              'pathname', 'process', 'processName', 'relativeCreated', 'thread',
                              'threadName', 'exc_info', 'exc_text', 'stack_info']:
                    doc[key] = value

        return doc

    def flush(self):
        """Flush buffered logs to Elasticsearch"""
        if not self.buffer:
            return

        try:
            # Index all buffered logs
            for doc in self.buffer:
                timestamp = datetime.fromisoformat(doc['@timestamp'])
                index = f"{self.index_name}-{timestamp.strftime('%Y.%m.%d')}"
                self.es.index(index=index, body=doc)

            self.buffer = []
        except Exception as e:
            # Use sys.stderr.write to avoid any potential logging recursion
            sys.stderr.write(f"ElasticsearchHandler: Error flushing logs to Elasticsearch: {e}\n")
            sys.stderr.flush()

    def close(self):
        """Close the handler and flush remaining logs"""
        try:
            self.flush()
        except Exception as e:
            import sys
            sys.stderr.write(f"ElasticsearchHandler: Error during final flush: {e}\n")
            sys.stderr.flush()
        try:
            self.es.close()
        except Exception as e:
            import sys
            sys.stderr.write(f"ElasticsearchHandler: Error closing Elasticsearch client: {e}\n")
            sys.stderr.flush()
        super().close()
        
def create_elastic_search_handler(app_name: str):
    es_host = os.getenv('LOGGING_ELASTICSEARCH_HOST', 'localhost')
    es_port = int(os.getenv('LOGGING_ELASTICSEARCH_PORT', 9200))
    es_index = os.getenv('LOGGING_ELASTICSEARCH_INDEX', 'python-apps-logs')
    
    host = f'http://{es_host}'
    
    # Initialize Elasticsearch client and index
    es_client = None
    try:
        es_client = Elasticsearch(f'{host}:{es_port}' )
        
        # Verify connection
        es_client.info()
        
        # Setup ILM policy for automatic log retention
        setup_ilm_policy(es_client)
        
        create_index_if_not_exists(es_client, es_index)
        
    except Exception as e:
        logging.warning(f"Centralized logging failed. Could not connect to Elasticsearch: {e}")
        raise(e)
    
    return ElasticsearchLoggingHandler(
        es_client=es_client,
        index_name=es_index,
        app_name=app_name,
        buffer_size=1)