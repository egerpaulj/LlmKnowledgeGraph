export OLLAMA_MODEL=qwen3:14b
export MLFLOW_USER_PROMPT_ID=NER_User@kt
export MLFLOW_SYSTEM_PROMPT_ID=NER_System@kt
export LOGGING_ELASTICSEARCH_HOST=localhost
python main.py --path-to-dir /home/user/Downloads/NoamBooks/politics
