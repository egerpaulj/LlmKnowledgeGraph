cd ../src/llm_ner_nel/evaluation

python main.py --csv example_data.csv --mlflow-experiment ner_release --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity --strategy ollama --model-name gemma3:4b;
python main.py --csv example_data.csv --mlflow-experiment ner_release --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity --strategy ollama --model-name gemma3:12b;
python main.py --csv example_data.csv --mlflow-experiment ner_release --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity --strategy ollama --model-name qwen3:14b;
python main.py --csv example_data.csv --mlflow-experiment ner_release --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity --strategy ollama --model-name qwen3:8b;
python main.py --csv example_data.csv --mlflow-experiment ner_release --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity --strategy ollama --model-name qwen3:4b;
python main.py --csv example_data.csv --mlflow-experiment ner_release --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity --strategy ollama --model-name magistral:24b;
python main.py --csv example_data.csv --mlflow-experiment ner_release --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity --strategy ollama --model-name rnj-1:latest;
python main.py --csv example_data.csv --mlflow-experiment ner_release --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity --strategy gpt-oss --model-name gpt-oss:20b;
python main.py --csv example_data.csv --mlflow-experiment ner_release --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity --strategy ollama --model-name granite4:3b;
python main.py --csv example_data.csv --mlflow-experiment ner_release --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity --strategy ollama --model-name ministral-3:3b;
python main.py --csv example_data.csv --mlflow-experiment ner_release --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity --strategy ollama --model-name ministral-3:8b;
python main.py --csv example_data.csv --mlflow-experiment ner_release --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity --strategy ollama --model-name ministral-3:14b;
python main.py --csv example_data.csv --mlflow-experiment ner_release --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity --strategy google --model-name gemini-2.5-flash-lite;
# output has reasoning - can't parse json -> python main.py --csv example_data.csv --model-name deepseek-r1:8b --mlflow-experiment ner --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity;
# output has reasoning - can't parse json -> python main.py --csv example_data.csv --model-name deepseek-r1:14b --mlflow-experiment ner --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity