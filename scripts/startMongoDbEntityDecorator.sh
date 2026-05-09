docker run -e OLLAMA_MODEL=qwen3:14b \
           -e OLLAMA_HOST=http://ollama:11434 \
           -e MONGODB_CONNECTION_STRING=mongodb://admin:secret@mongodb:27017 \
           -e MLFLOW_TRACKING_HOST=http://mlflow:5000 \
           --network development_network \
           --rm \
           --name mongodb-entity-decorator \
           --hostname mongodb-entity-decorator \
           mongodb-entity-decorator