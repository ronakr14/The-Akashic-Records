---
id: jrwggsosur3o3rchcv8civu
title: Cheatsheet
desc: ''
updated: 1752508142849
created: 1752508142120
---

## 🧾 Cheat Sheets

* **Ollama CLI Basics**:

```bash
ollama pull llama2
ollama run llama2
ollama serve
```

* **Ollama Python API**:

```python
import requests

response = requests.post(
    'http://localhost:11434/api/generate',
    json={'model': 'llama2', 'prompt': 'Explain quantum computing simply.'}
)
print(response.json()['response'])
```

* **Custom Model Mod File**:

```bash
FROM llama2
SYSTEM "You are a helpful AI assistant specialized in SQL generation."
```

* **LangChain Ollama Integration**:

```python
from langchain.llms import Ollama

llm = Ollama(model="llama2")
response = llm("Summarize this document.")
```

* **RAG Architecture (Rough Sketch)**:

1. Load documents via `PyPDFLoader`.
2. Store embeddings in ChromaDB.
3. Query ChromaDB for relevant chunks.
4. Feed results to Ollama model via API for answer generation.

* **Serve via FastAPI**:

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/ask/")
async def ask_ollama(query: str):
    response = requests.post('http://localhost:11434/api/generate',
                             json={'model': 'mistral', 'prompt': query})
    return {"response": response.json()['response']}
```
