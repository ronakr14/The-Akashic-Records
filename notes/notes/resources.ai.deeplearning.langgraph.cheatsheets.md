---
id: 3o3x5p7pzy8tbz547u0j2r1
title: Cheatsheets
desc: ''
updated: 1752507856022
created: 1752507855538
---

## 🧾 Cheat Sheets

* **Basic Graph Node**:

```python
import langgraph

def node_logic(state):
    # Your LLM chain or custom logic
    return {"response": "Processed: " + state["input"]}

graph = langgraph.Graph()
graph.add_node("processor", node_logic)
graph.add_edge("start", "processor")
graph.add_edge("processor", "end")
```

* **Conditional Edge**:

```python
def branching_logic(state):
    if "math" in state["input"]:
        return "calculator_node"
    return "general_llm_node"

graph.add_conditional_edges("router_node", branching_logic)
```

* **Cycles / Loops Example**:

```python
# From 'review' node, return to 'refiner' node until condition met
graph.add_edge("review", "refiner")
```

* **Run Graph**:

```python
result = graph.run({"input": "Hello, world!"})
```
