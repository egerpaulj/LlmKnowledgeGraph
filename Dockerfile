FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


ENV RABBITMQ_HOST=localhost
ENV RABBITMQ_PORT=5672
ENV RABBITMQ_VHOST=/
ENV RABBITMQ_QUEUE=default
ENV RABBITMQ_USER=guest
ENV RABBITMQ_PASSWORD=guest
ENV OLLAMA_HOST=http://localhost:11434
ENV OLLAMA_MODEL=default-model
ENV NEO4J_URI=neo4j://localhost:7687
ENV NEO4J_USERNAME=neo4j
ENV NEO4J_PASSWORD=password

CMD ["python", "consumer.py"]
