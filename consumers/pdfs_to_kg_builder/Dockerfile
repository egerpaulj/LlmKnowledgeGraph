FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


ENV OLLAMA_HOST=http://localhost:11434
ENV OLLAMA_MODEL=default-model
ENV NEO4J_URI=neo4j://localhost:7687
ENV NEO4J_USERNAME=neo4j
ENV NEO4J_PASSWORD=password
ENV MLFLOW_TRACKING_HOST=http://localhost:5050
ENV MLFLOW_SYSTEM_PROMPT_ID=NER_System/@relationship
ENV MLFLOW_USER_PROMPT_ID=NER_User/@relationship



CMD ["python", "main.py", "--path-to-dir", "/mnt"]
