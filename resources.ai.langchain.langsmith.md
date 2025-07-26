---
id: qfpcvapc2vp11g0rzr2fxjg
title: Langsmith
desc: ''
updated: 1753517715371
created: 1753517710277
---
tags: [master, langsmith, langchain, debugging, evaluation, llmops, agentic-workflows]

---

## 📌 Topic Overview

**LangSmith** is an **LLMOps platform** by LangChain that helps you **debug, trace, evaluate, and monitor** LLM-based applications — especially those built with LangChain.

Where LangChain is your “framework” and Langflow your “UI,” **LangSmith is your black box recorder and QA lab.** It shows how your agents, tools, prompts, and chains behave across inputs, in real-time or retrospectively.

> 🧠 Think of LangSmith as a **New Relic + Postman + GitHub Copilot** for LLM pipelines.

LangSmith helps you:
- Visualize execution traces across chains/tools/agents
- Evaluate outputs via human or LLM feedback
- Log and version your experiments
- Monitor production workflows
- Compare prompts and model performance over time

---

## 🚀 80/20 Roadmap

| Stage | Concept                  | Why It Matters                                               |
|-------|--------------------------|---------------------------------------------------------------|
| 1️⃣    | Project & Run Tracking    | Centralized logging for LangChain chains                     |
| 2️⃣    | Execution Tracing         | Visual debugger for complex chains and agent tool calls      |
| 3️⃣    | Dataset Logging & Versioning | Input/output capture for evaluation and CI/CD            |
| 4️⃣    | Evaluation + Feedback     | Auto/Manual scoring to judge model responses                 |
| 5️⃣    | Prompt Testing & Comparison | A/B testing and regression of prompt chains                |
| 6️⃣    | LLM Tracing & Token Logs  | Monitor latency, token usage, and model response times       |
| 7️⃣    | Production Monitoring     | Alerts, dashboards, and tracing for live apps                |

---

## 🛠️ Practical Tasks

- ✅ Create a LangSmith account and get an API key  
- ✅ Enable LangSmith tracing in your LangChain environment  
- ✅ Track a simple chain execution  
- ✅ View the trace tree of a tool-using agent  
- ✅ Log multiple runs into a **Dataset**  
- ✅ Evaluate outputs with LLM-based feedback  
- ✅ Create a comparison report between prompt versions  
- ✅ Use LangSmith CLI to push data for offline testing  
- ✅ Export traces for auditing/debugging  

---

## 🧾 Cheat Sheets

### ▶️ Install LangSmith

```bash
pip install langsmith
````

### 🌐 Set Environment Variables

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=sk-...
export LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
export LANGCHAIN_PROJECT=my-agent-project
```

Add to `.env` or shell profile for persistence.

---

### 🧠 Log a Chain to LangSmith

```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

template = "Translate the following to French: {text}"
prompt = PromptTemplate(input_variables=["text"], template=template)

chain = LLMChain(llm=OpenAI(), prompt=prompt)
result = chain.run("I love LangSmith")
```

This will auto-log into your LangSmith dashboard under the project name.

---

### 🔍 Visual Trace Tree

* Shows each step: Prompt → LLM Call → Tool Use → Final Output
* Drill down into input/output, tokens, model name, latency

---

### 📁 Datasets

* Group of runs with inputs & outputs
* Useful for regression testing and benchmarking

```bash
langsmith dataset create "prompt-tests"
langsmith run --dataset "prompt-tests" ...
```

---

### 📊 Evaluation

```python
from langsmith.evaluation import RunEvaluator

evaluator = RunEvaluator.from_llm()
evaluator.evaluate_run(run_id="1234")
```

Or use LangSmith UI to run **LLM-based or human evaluations**.

---

## 🎯 Progressive Challenges

| Level           | Challenge                                                            |
| --------------- | -------------------------------------------------------------------- |
| 🥉 Beginner     | Enable tracing and log a simple LLMChain                             |
| 🥈 Intermediate | Build a Dataset and auto-evaluate 10 test prompts                    |
| 🥇 Advanced     | Compare performance between two prompts or model versions            |
| 🏆 Expert       | Deploy a production app with full tracing, alerting, and evaluations |

---

## 🎙️ Interview Q\&A

* **Q:** What is LangSmith used for?
* **Q:** How does LangSmith improve debugging of LLM pipelines?
* **Q:** Can you compare two prompt versions in LangSmith?
* **Q:** What types of evaluations does LangSmith support?
* **Q:** How do you integrate LangSmith in CI/CD or a QA pipeline?

---

## 🛣️ Next Tech Stack Recommendations

* **LangChain** — LangSmith is designed for it, but can work with custom code via API
* **LLM Benchmarking Tools** — Like PromptLayer, Trulens, or Ragas (LangSmith > all)
* **DVC / Weights & Biases** — For model versioning alongside trace/version management
* **Streamlit / FastAPI** — Embed LangSmith-traced components in apps
* **LangGraph** — Build flow control logic with LangSmith as a trace and feedback layer
* **S3 / Vector DBs / Postgres** — Log external artifacts from LangChain chains

---

## 🧬 Tactical Philosophy

> “If LangChain is how you build, **LangSmith is how you know it works.**”

✅ Developer observability for LLM apps
🧪 QA testing for language pipelines
🧭 Auditable, reproducible traces
⚖️ Trustworthy evaluation methods
📈 Actionable insights before you go to prod
