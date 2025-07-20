---
id: gkdgsj2zmuuv8q5ldkgkavv
title: Chromadb
desc: ''
updated: 1753021849821
created: 1753021302258
---

## 📌 Topic Overview

**ChromaDB** is:

* An **open-source, lightweight vector database**.
* Stores document embeddings (vectors).
* Powers **semantic search** and **retrieval-based pipelines**.
* Used as the core retrieval layer in modern RAG architectures.

Why it matters:

* You need ChromaDB to let LLMs “look up” real data.
* Enables private, local, fast, and scalable document search.

Compare it to:

* Pinecone (SaaS), Weaviate (heavier), FAISS (less feature-rich).
* **ChromaDB = lightweight, local-first Pinecone alternative.**

---

## ⚡ 80/20 Roadmap

| Stage  | Focus Area                          | Why?                                  |
| ------ | ----------------------------------- | ------------------------------------- |
| **1**  | Embeddings Basics                   | Understand what you're storing.       |
| **2**  | ChromaDB Installation & Collections | Core data structures.                 |
| **3**  | Adding Documents + Embeddings       | Data ingestion pipeline.              |
| **4**  | Querying via Similarity Search      | Semantic search foundation.           |
| **5**  | Persistent Storage                  | Keep your index across sessions.      |
| **6**  | LangChain + ChromaDB Integration    | Plug into LLM pipelines.              |
| **7**  | Advanced Filters                    | Filter search results by metadata.    |
| **8**  | Multi-Document Retrieval            | Power your RAG systems.               |
| **9**  | API Wrapping                        | Build custom endpoints over ChromaDB. |
| **10** | Deployment & Scaling                | Serve ChromaDB as a service.          |

---

## 🚀 Practical Tasks

| Task                                                                               | Description |
| ---------------------------------------------------------------------------------- | ----------- |
| 🔥 Install ChromaDB (`pip install chromadb`).                                      |             |
| 🔥 Create a collection and add text documents + embeddings.                        |             |
| 🔥 Use OpenAI / Ollama / Sentence Transformers to generate embeddings.             |             |
| 🔥 Query ChromaDB for semantic similarity searches.                                |             |
| 🔥 Set up ChromaDB with persistence to store your DB across restarts.              |             |
| 🔥 Build a RAG pipeline: use ChromaDB + Ollama to answer questions from documents. |             |
| 🔥 Expose ChromaDB queries via FastAPI endpoint.                                   |             |
| 🔥 Integrate ChromaDB as retriever in LangChain RetrievalQA pipeline.              |             |

---

## 🧾 Cheat Sheets

* **Basic Setup**:

```python
import chromadb
client = chromadb.Client()

collection = client.create_collection(name="my_documents")
collection.add(
    documents=["Doc about AI", "Doc about SQL"],
    embeddings=[[0.1, 0.2, ...], [0.4, 0.5, ...]],  # Use actual embeddings
    ids=["doc1", "doc2"]
)
```

* **Query by Similarity**:

```python
results = collection.query(
    query_embeddings=[[0.1, 0.2, ...]],
    n_results=3
)
print(results)
```

* **Using Persistent Storage**:

```python
client = chromadb.PersistentClient(path="/path/to/db")
```

* **Generating Embeddings (e.g., OpenAI)**:

```python
from openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings().embed_documents(["Text1", "Text2"])
```

* **LangChain Retriever Setup**:

```python
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

db = Chroma(
    persist_directory="./db",
    embedding_function=OpenAIEmbeddings()
)
retriever = db.as_retriever()
```

---

## 🎯 Progressive Challenges

| Level           | Challenge                                                          |
| --------------- | ------------------------------------------------------------------ |
| 🥉 Easy         | Build and query a local ChromaDB collection.                       |
| 🥈 Intermediate | Build a document Q\&A system using ChromaDB + Ollama.              |
| 🥇 Expert       | Integrate ChromaDB retriever into a LangChain RAG pipeline.        |
| 🏆 Black Belt   | Serve ChromaDB queries via FastAPI for remote semantic search API. |

---

## 🎙️ Interview Q\&A

* **Q:** What is ChromaDB and why use it over FAISS or Pinecone?
* **Q:** How does semantic search work in ChromaDB?
* **Q:** What are embeddings? Why do we store them?
* **Q:** How do you persist ChromaDB data?
* **Q:** How does ChromaDB enable RAG pipelines?

---

## 🛣️ Next Tech Stack Recommendation

After mastering ChromaDB:

* **Weaviate / Qdrant** — For large-scale or SaaS-based vector search.
* **Ollama + Local LLaMA** — To build private RAG systems.
* **LangGraph + ChromaDB** — Graph-based control flow for retrieval tasks.
* **Dockerize ChromaDB API** — For scalable remote vector DB serving.
* **Streamlit / Gradio** — Build dashboards over your document search.

---

## 🎩 Pro Ops Tips

* Always persist your DB in production (`PersistentClient`).
* Use **metadata** to tag documents for advanced filtered retrieval.
* Pre-compute embeddings during ingestion for scalability.
* Treat ChromaDB as your **AI Knowledge Base**.
* Backup your persisted ChromaDB folder regularly.

---

## ⚔️ Tactical Philosophy

**ChromaDB transforms static documents into searchable, retrievable AI knowledge.**

Think of it as your LLM’s external memory. No more hallucinations—only grounded, factual answers.

---
