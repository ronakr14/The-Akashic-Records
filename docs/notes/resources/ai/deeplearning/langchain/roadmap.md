# Roadmap

## ⚡ 80/20 Roadmap

Focus on **pipelines + modular systems** to avoid prompt spaghetti.

| Stage  | Focus Area                                          | Why?                                     |
| ------ | --------------------------------------------------- | ---------------------------------------- |
| **1**  | LLM Wrappers (`LLMChain`)                           | Standard method to call any LLM.         |
| **2**  | Prompt Templates                                    | Keep prompts reusable and parameterized. |
| **3**  | Memory (ConversationBufferMemory)                   | Maintain chat state.                     |
| **4**  | Chains (`SequentialChain`, `SimpleSequentialChain`) | Multi-step workflows.                    |
| **5**  | Tools & Agents                                      | Enable reasoning + tool usage.           |
| **6**  | Document Loaders + Text Splitters                   | Process data sources for RAG.            |
| **7**  | Vector Stores (FAISS, ChromaDB, Pinecone)           | Enable semantic search.                  |
| **8**  | Retrieval QA Chain                                  | The backbone of RAG pipelines.           |
| **9**  | AsyncLangChain (Optional)                           | For scalable, concurrent chains.         |
| **10** | Serving via FastAPI                                 | Deploy AI workflows as APIs.             |