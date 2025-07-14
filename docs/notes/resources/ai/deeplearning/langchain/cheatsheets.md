# Cheatsheets

## 🧾 Cheat Sheets

- **LLMChain with Prompt Template**:

```python
from langchain import LLMChain, OpenAI, PromptTemplate

llm = OpenAI(model="gpt-3.5-turbo")
prompt = PromptTemplate(template="Translate '{text}' to French.", input_variables=["text"])
chain = LLMChain(llm=llm, prompt=prompt)

response = chain.run(text="Hello, how are you?")
```

- **RAG Pipeline (RetrievalQA Chain)**:

```python
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA

# Load and index documents
loader = PyPDFLoader("manual.pdf")
docs = loader.load()
db = FAISS.from_documents(docs, embedding)

# RAG Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    retriever=db.as_retriever(),
    chain_type="stuff"
)
response = qa_chain.run("How do I reset my password?")
```

- **Agent with Tools**:

```python
from langchain.agents import initialize_agent, Tool
from langchain.tools.python.tool import PythonREPLTool

tools = [Tool(name="Python", func=PythonREPLTool().run, description="Run Python code")]
agent = initialize_agent(tools, OpenAI(), agent="zero-shot-react-description")
response = agent.run("What is 23 squared?")
```