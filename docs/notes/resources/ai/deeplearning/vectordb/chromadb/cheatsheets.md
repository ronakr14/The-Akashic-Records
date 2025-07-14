# Cheatsheets

## 🧾 Cheat Sheets

- **Basic Setup**:

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

- **Query by Similarity**:

```python
results = collection.query(
    query_embeddings=[[0.1, 0.2, ...]],
    n_results=3
)
print(results)
```

- **Using Persistent Storage**:

```python
client = chromadb.PersistentClient(path="/path/to/db")
```

- **Generating Embeddings (e.g., OpenAI)**:

```python
from openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings().embed_documents(["Text1", "Text2"])
```

- **LangChain Retriever Setup**:

```python
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

db = Chroma(
    persist_directory="./db",
    embedding_function=OpenAIEmbeddings()
)
retriever = db.as_retriever()
```