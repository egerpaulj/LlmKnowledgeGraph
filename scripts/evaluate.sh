cd ../src/llm_ner_nel/evaluation
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@deepseek --mlflow-user-prompt-id NER_User@deepseek --strategy ollama-slim --model-name deepseek-r1:14b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@deepseek --mlflow-user-prompt-id NER_User@deepseek --strategy ollama-slim --model-name deepseek-r1:8b;

python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy google --model-name gemini-2.5-flash-lite;

python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy google --model-name gemini-2.5-flash-lite;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy google --model-name gemini-3-flash-preview;


python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy google --model-name gemini-3-flash-preview;

python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy openai --model-name o4-mini;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy openai-slim --model-name o4-mini;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy openai-slim --model-name o4-mini;


python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy openai --model-name gpt-5-mini;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy openai-slim --model-name gpt-5-mini;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy openai-slim --model-name gpt-5-mini;

python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name gemma3:12b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy ollama-slim --model-name gemma3:12b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy ollama-slim --model-name gemma3:12b;

python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy openai --model-name gpt-4o-mini;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy openai-slim --model-name gpt-4o-mini;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy openai-slim --model-name gpt-4o-mini;

python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy google-slim --model-name gemini-3-flash-preview;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy google-slim --model-name gemini-3-flash-preview;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy google --model-name gemini-3-flash-preview;



python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy openai --model-name gpt-5-nano;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy openai --model-name gpt-5-mini;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy openai --model-name o4-mini;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy openai --model-name gpt-5-mini;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy openai --model-name gpt-4o-mini
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy openai --model-name o4-mini;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy openai --model-name gpt-5-nano;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy openai --model-name gpt-5-mini;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy openai --model-name gpt-5-mini;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy openai --model-name gpt-4o-mini;


python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name gemma3:4b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name gemma3:12b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name qwen3:14b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name qwen3:8b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name magistral:24b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name rnj-1:latest;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy gpt-oss --model-name gpt-oss:20b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name granite4:3b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name ministral-3:3b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name ministral-3:8b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name ministral-3:14b;

python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name gemma3:4b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name gemma3:12b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name qwen3:14b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name qwen3:8b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name magistral:24b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name rnj-1:latest;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy gpt-oss --model-name gpt-oss:20b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name granite4:3b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name ministral-3:3b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name ministral-3:8b;
python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name ministral-3:14b;
output has reasoning - can't parse json -> python main.py --csv example_data.csv --model-name deepseek-r1:8b --mlflow-experiment ner --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity;
output has reasoning - can't parse json -> python main.py --csv example_data.csv --model-name deepseek-r1:14b --mlflow-experiment ner --mlflow-system-prompt-id NER_System@entity --mlflow-user-prompt-id NER_User@entity
output parsing issues -> python main.py --csv example_data.csv --mlflow-experiment ner_nohp --mlflow-system-prompt-id NER_System@basic --mlflow-user-prompt-id NER_User@basic --strategy ollama --model-name qwen3:4b;