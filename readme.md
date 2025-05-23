# LLM Knowledge Graph
Use an LLM to generate a knowledge graph.

The purpose of the library is to extract entities and their relationships without a pre-defined schema.

**Input**: Paragraphs of text

**Output**: Nodes and Relationships

**Output**: Merge the nodes into the Knowledge Graph database

E.g.
```python
from knowledge_graph import KnowledgeGraph

graph = KnowledgeGraph(model="gemma3:12b")

text = '''Australia’s centre-left prime minister, Anthony Albanese, has won a second term with a crushing victory over the opposition, whose rightwing leader, Peter Dutton, failed to brush off comparisons with Donald Trump and ended up losing his own seat.
Australians have voted for a future that holds true to these values, a future built on everything that brings us together as Australians, and everything that sets our nation apart from the world'''

graph.add_to_graph(text, "https://en.wikipedia.org/wiki/Vincent_de_Groof", "Wikipedia"))
```

<img src=image.png>

#### Try it using a Jupyter Notebook:

[working_example.ipynb](working_example.ipynb)

Use the conda environment:

<img src=jupyter.png>


## Dependencies

- Neo4j Database
- Python
- Local LLM (Ollama)

### Environment setup

#### Neo4j

Run a local instance of the Neo4J database

- Run the startNeo4j.sh script
- Or run the following

```bash
docker run \
    --name neo4j \
    -d --rm \
    -p 7474:7474 -p 7687:7687 \
    --name neo4j-apoc \
    --volume=./data:/data \
    -e NEO4J_AUTH=neo4j/password \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4J_PLUGINS=\[\"apoc\"\] \
    neo4j:2025.03
```

Verify access to Neo4J:

http://localhost:7474/browser/

- Username: neo4j
- Password: password

#### Python dependencies

Install the following dependencies:

```bash
pip install -U py2neo
pip install -U pydantic
pip install -U ollama
```

Alternatively, setup a conda environment and install the dependencies:

```bash
conda create -n knowledge-graph python=3.10
conda activate knowledge-graph
pip install -U py2neo
pip install -U pydantic
pip install -U ollama
# if running Jupyter notebook on VSCODE
pip install -U ipykernel
```

#### Local LLM - Ollama

Run a local LLM using OLLAMA.

- Download and install OLLAMA:
https://ollama.com/download

- Download the LLM Model

```bash
ollama run gemma3:12b
```

Note: if you have a GPU or an environment with High Bandwidth Memory, then it is recommended to run a larger model.

E.g.
**gemma3:27b**

Note: when changing the model, specify the model name

E.g.

```python
from knowledge_graph import KnowledgeGraph

graph = KnowledgeGraph(model="gemma3:27b")
```

## Hyper parameters and prompt

The LLM prompt and hyper parameters can be defined, these would help to refine the expected output for concrete use-cases:

```python
class LlmConfig:
        
    model: str
    temperature: float
    top_k: int
    top_p: float
    max_tokens: int
    repeat_penalty: float
    frequency_penalty: float
    presence_penalty: float
    typical_p: float
    num_thread: int
```

The prompts and examples can be adapted in:
- System prompt
- Examples
- User prompt

**knowledge_graph.py**

```bash
system_prompt_1 = "prompt"
examples = "positive extracted examples"

def generate_prompt(self, text, examples):

```

## Pipeline: knowledge graph ingestion pipeline
Use RabbitMQ to Publish/Consume messages.

The messages will be processed and merged to the knowledge graph

<img src=kt_pipeline.png/>

Message format:
```json
{
  "src": "https://en.wikipedia.org/wiki/Vincent_de_Groof",
  "src_type": "Newspaper",
  "text": "Vincent de Groof (6 December 1830 – 9 July 1874) was a Dutch-born Belgian early pioneering aeronaut. He created an early model of an ornithopter and successfully demonstrated its use before fatally crashing the machine in London, UK.[1] "
}

```

### Pipeline dependecy RabbitMq

Start rabbitmq:
```bash
docker run -d --rm --network development_network --hostname rabbitmq --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3.8.12-rc.1-management
```



## Docker

The pipeline consumer can be setup to run in a docker container.

Build the image:
```bash
docker build -t kt-consumer .
```

Run the container:
```bash
docker run -e RABBITMQ_PORT=5672 \
           -e RABBITMQ_HOST=rabbitmq \
           -e RABBITMQ_VHOST=dev \
           -e RABBITMQ_QUEUE=chomsky.info \
           -e RABBITMQ_USER=guest \
           -e RABBITMQ_PASSWORD=guest \
           -e OLLAMA_MODEL=llama3.2 \
           -e OLLAMA_HOST=http://ollama:11434 \
           -e NEO4J_URI=bolt://neo4j-apoc:7687 \
           -e NEO4J_USERNAME=neo4j \
           -e NEO4J_PASSWORD=password \
           --network development_network \
           --rm \
           --name knowledge_consumer \
           --hostname knowledge_consumer \
           kt-consumer
```

Ollama should be running in a docker container; or a network route should be available.

Run the following for a CPU-Only ollama instance:

```bash
docker run -d --rm 
    -v /usr/share/ollama/.ollama:/root/.ollama \
    -p 11434:11434 \
    --network development_network \
    --name ollama \
    --hostname ollama  \
    ollama/ollama

```

Note: replace the path **/usr/share/ollama/.ollama** to the host's ollama model path


## License

Copyright (C) 2025  Paul Eger

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
