---
id: 7peud0h3e3y8artxcdsjtlo
title: Cheatsheets
desc: ''
updated: 1752507996386
created: 1752507994967
---

## 🧾 Cheat Sheets

* **Tool Creation**:

```python
from langchain.tools import Tool

def my_tool_function(input):
    return input.upper()

tools = [Tool(name="UppercaseTool", func=my_tool_function, description="Converts text to uppercase.")]
```

* **Agent Setup (Zero-Shot ReAct)**:

```python
from langchain.agents import initialize_agent, AgentType

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

response = agent.run("What is 45 squared?")
```

* **Tool Using Python REPL Example**:

```python
from langchain.tools.python.tool import PythonREPLTool

tools = [
    Tool(
        name="Python",
        func=PythonREPLTool().run,
        description="Useful for solving math problems or code execution."
    )
]
```

* **Memory for Stateful Agents**:

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
agent = initialize_agent(..., memory=memory)
```

* **Deploy Agent via FastAPI**:

```python
from fastapi import FastAPI
app = FastAPI()

@app.post("/agent/")
async def query_agent(query: str):
    return {"response": agent.run(query)}
```
