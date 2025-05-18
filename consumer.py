#!/usr/bin/env python
import pika
import sys
import os
import json
from graph import KnowledgeGraph

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the minimum log level
    format='%(asctime)s - %(levelname)s - %(message)s',
)

class Consumer:
    def __init__(self, host, port, virtual_host, queue_name, username, password, ollama_host, ollama_model):
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.queue_name = queue_name
        self.username = username
        self.password = password
        self.graph = KnowledgeGraph(model=ollama_model, ollama_host=ollama_host)
        self.connection = None
        self.channel = None
        logging.info(ollama_host)

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.virtual_host,
                credentials=credentials
            )
        )
        self.channel = self.connection.channel()

    def start_consuming(self):
        if self.channel is None:
            raise Exception("Channel is not initialized. Call connect() first.")

        def callback(ch, method, properties, body):
            try:
                message = json.loads(body)
                src = message.get('src')
                src_type = message.get('src_type')
                text = message.get('text')
                logging.info(f"[x] Received: src={src}, text={text}")
                
                self.graph.add_to_graph(text=text, src=src, src_type=src_type)
            except Exception as e:
                logging.error(f"[!] Error processing message: {e}")

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback,
            auto_ack=True
        )

        logging.info(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

if __name__ == '__main__':
    try:
        host = os.getenv('RABBITMQ_HOST', 'localhost')
        port = int(os.getenv('RABBITMQ_PORT', '5672'))
        vhost = os.getenv('RABBITMQ_VHOST', 'dev')
        queue = os.getenv('RABBITMQ_QUEUE', 'chomsky.info')
        username = os.getenv('RABBITMQ_USER', 'guest')
        password = os.getenv('RABBITMQ_PASSWORD', 'guest')
        ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2')

        consumer = Consumer(
            host=host,
            port=port,
            virtual_host=vhost,
            queue_name=queue,
            username=username,
            password=password,
            ollama_host=ollama_host,
            ollama_model=ollama_model
        )
        consumer.connect()
        consumer.start_consuming()
    except KeyboardInterrupt:
        logging.info('Interrupted')
        try:
            logging.info("exiting")
            sys.exit(0)
        except SystemExit:
            os._exit(0)
