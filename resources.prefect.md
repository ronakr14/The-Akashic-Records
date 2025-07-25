---
id: 3im1ts1opqneywcb36s9qkv
title: Prefect
desc: ''
updated: 1753457687585
created: 1753457682423
---
tags: [master, orchestration, prefect, data-engineering, workflow-automation, pipelines]

## 📌 Topic Overview

**Prefect** is a next-gen dataflow orchestration tool designed to fix the shortcomings of Airflow. It lets you build, run, and monitor data pipelines—locally or in the cloud—using Pythonic code with **less friction**, **better observability**, and **dynamic workflows** out of the box.

It ditches the static DAG model and embraces **functional flows** with native support for async, parameters, retries, caching, and easy local testing.

> ⚡️“If Airflow feels like configuring a Boeing 747, Prefect is like flying a drone with your phone.”

---

## 🚀 80/20 Roadmap

| Stage | Concept                     | Why It Matters                                                   |
|-------|-----------------------------|------------------------------------------------------------------|
| 1️⃣    | Flows & Tasks               | Core abstraction. Python functions wrapped as flows/tasks        |
| 2️⃣    | Parameters                  | Dynamically pass data into flows/tasks                           |
| 3️⃣    | Retry, Timeout, & Caching  | Make workflows resilient and efficient                           |
| 4️⃣    | State & Logging             | Track task status, outputs, and failures                         |
| 5️⃣    | Deployment & Schedules     | Move from local dev to scheduled production flows                |
| 6️⃣    | Prefect Cloud vs Local     | Choose between hosted observability or self-managed              |
| 7️⃣    | Blocks & Secrets           | Manage credentials and integrations cleanly                      |
| 8️⃣    | Infrastructure Abstraction | Run flows on Docker, Kubernetes, or serverless platforms         |
| 9️⃣    | Flow of Flows              | Compose larger workflows with subflows                           |
| 🔟    | Integrations                | Use with dbt, GCS, Snowflake, Slack, GitHub, AWS, etc.           |

---

## 🛠️ Practical Tasks

- ✅ Create a flow with two dependent tasks  
- ✅ Add retry logic and timeout on flaky API calls  
- ✅ Use flow parameters to pass dynamic values  
- ✅ Store AWS creds securely using Prefect Blocks  
- ✅ Schedule a flow using an interval schedule  
- ✅ Trigger a flow manually via CLI or UI  
- ✅ Send Slack alerts on failure via notification block  
- ✅ Cache expensive calls for better performance  
- ✅ Deploy a Docker-based flow to run on ECS or K8s  
- ✅ Use `flow_run_name` templating for traceable jobs  

---

## 🧾 Cheat Sheets

### 🧪 Simple Flow

```python
from prefect import flow, task

@task
def fetch_data():
    return {"value": 42}

@task
def transform(data):
    return data["value"] * 2

@flow
def my_etl():
    raw = fetch_data()
    result = transform(raw)
    print(f"Transformed result: {result}")

my_etl()
````

### 🧰 With Parameters and Retry

```python
from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(retries=3, retry_delay_seconds=10, cache_key_fn=task_input_hash, cache_expiration=timedelta(minutes=30))
def api_call(param):
    return f"Response for {param}"

@flow
def parameterized_flow(param: str):
    result = api_call(param)
    print(result)

parameterized_flow("🚀")
```

---

## 🎯 Progressive Challenges

| Level           | Challenge                                                                  |
| --------------- | -------------------------------------------------------------------------- |
| 🥉 Beginner     | Build a flow that reads, transforms, and prints JSON                       |
| 🥈 Intermediate | Add retries and caching for unstable external API calls                    |
| 🥇 Advanced     | Chain multiple flows together using `flow-of-flows`                        |
| 🏆 Expert       | Deploy Prefect with K8s agent, Dockerized flows, and alerting integrations |

---

## 🎙️ Interview Q\&A

* **Q:** How does Prefect differ from Airflow?
* **Q:** What’s a `flow`, what’s a `task`, and how do they relate?
* **Q:** How do retries and caching work in Prefect?
* **Q:** How can flows be scheduled and deployed to production?
* **Q:** What are blocks, and how do they help manage secrets/infrastructure?

---

## 🛣️ Next Tech Stack Recommendations

* **DVC / MLflow** — Pair with Prefect for model versioning & orchestration
* **dbt + Snowflake** — Use Prefect to orchestrate dbt + warehouse jobs
* **Slack / Discord / PagerDuty** — Notification blocks for observability
* **Docker + ECS / Kubernetes** — Deploy Prefect agents and flows in containers
* **GitHub Actions** — Trigger flows on git events or release deployments
* **LangChain / LLM Workflows** — Prefect can orchestrate AI agents & pipelines

---

## 🧠 Pro Tips

* Use the **@task decorator** instead of writing static DAGs
* Store secrets/configs in Blocks—not in code or env vars
* Cache long-running computations to avoid recomputation
* Use `flow_run_name` to auto-tag runs for traceability
* Use `tags` to selectively run or skip flows in CI/CD pipelines

---

## 🧬 Tactical Philosophy

> “Workflows should be *code-first*, *cloud-agnostic*, and *developer-joyful*.”

📦 Treat flows as reusable microservices
🔁 Bake in retries, caching, observability from day one
🔐 Use Blocks for secure, pluggable storage & secrets
🌍 Cloud-native: flows should run anywhere with minimal friction
🛠️ Don’t orchestrate workflows manually—delegate it to Prefect!

---

