---
title: "FastAPI CLI Decorator"
source: "https://chatgpt.com/c/6a12e744-ef2c-8320-b10f-cb82f77dd559"
author:
published:
created: 2026-05-26
description: "ChatGPT conversation with 16 messages"
tags:
  - "clippings"
---
**ChatGPT said**

Yes—you can do all of that, but if you try to bolt it on ad-hoc, it’ll turn into a fragile mess. The clean way is to treat this as a **thin execution platform** with pluggable capabilities.

What you’re really building is:

> “One function → multiple execution surfaces (CLI, API, async job, webhook trigger)”

That’s a strong abstraction if you keep the boundaries disciplined.

---

```
┌──────────────┐
           │   Function   │  ← your business logic (pure)
           └──────┬───────┘
                  │
   ┌──────────────┼──────────────┐
   │              │              │
CLI Runner     API Layer     Queue Worker
   │              │              │
Typer        FastAPI       Celery Worker
   │              │              │
   └──────┬───────┴───────┬──────┘
          │               │
      Redis           Observability
```

---

## ⚙️ 1. Core Decorator (single source of truth)

Now it registers everything: API + CLI + async capability.

```python
# decorators.py
from registry import register_route, register_task, register_cli

def expose(
    path: str = None,
    method: str = "POST",
    auth: bool = True,
    rate_limit: int = 10,
    async_task: bool = False,
):
    def decorator(func):
        name = func.__name__
        route_path = path or f"/{name.replace('_', '-')}"
        
        config = {
            "name": name,
            "func": func,
            "path": route_path,
            "method": method,
            "auth": auth,
            "rate_limit": rate_limit,
            "async_task": async_task,
        }

        register_route(config)
        register_cli(config)

        if async_task:
            register_task(config)

        return func
    return decorator
```

This becomes your **control plane**.

---

## 🔴 2. Redis (rate limit + state + queue backend)

Use Redis as:

- rate limiter
- Celery broker
- result backend
- caching layer (later)
```python
# redis_client.py
import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0)
```

---

## 🚦 3. Proper Rate Limiting (Redis-backed)

```python
def check_rate_limit(path: str, limit: int, client_ip: str):
    key = f"rate:{client_ip}:{path}"
    current = redis_client.incr(key)

    if current == 1:
        redis_client.expire(key, 60)

    if current > limit:
        raise Exception("Rate limit exceeded")
```

This is **atomic + production-safe**.

---

## ⚡ 4. Async Job Queue (Celery)

Use Celery.

```python
# worker.py
from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)
```

---

### Dynamic Task Registration

```python
# task_registry.py
from worker import celery_app

TASKS = {}

def register_task(config):
    func = config["func"]
    name = config["name"]

    @celery_app.task(name=name)
    def task_wrapper(**kwargs):
        return func(**kwargs)

    TASKS[name] = task_wrapper
```

---

## 🌐 5. FastAPI Layer (sync + async execution)

```python
# app.py
from fastapi import FastAPI, Request
from registry import ROUTES
from task_registry import TASKS

app = FastAPI()

def create_endpoint(config):
    func = config["func"]

    async def endpoint(request: Request, **kwargs):
        # rate limit
        check_rate_limit(config["path"], config["rate_limit"], request.client.host)

        # async execution
        if config["async_task"]:
            task = TASKS[config["name"]].delay(**kwargs)
            return {"task_id": task.id, "status": "queued"}

        return func(**kwargs)

    return endpoint
```

---

## 🧪 6. CLI Layer (same function, no duplication)

Use Typer.

```python
# cli_app.py
import typer

cli = typer.Typer()

def register_cli(config):
    func = config["func"]
    cli.command()(func)
```

Now:

```
python main.py add --a 1 --b 2
```

Same function. No duplication.

---

## 🔍 7. Observability (don’t skip this)

At minimum:

### Logging

```python
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("app")
```

### Structured Logs

```python
logger.info({
    "event": "api_call",
    "route": config["path"],
    "params": kwargs
})
```

---

### Metrics + Tracing (real systems)

Use:

- Prometheus (metrics)
- Grafana (dashboards)
- OpenTelemetry (tracing)

If you skip this, debugging async jobs later will hurt.

---

## 🔗 8. Automation Trigger (n8n / webhook)

Expose endpoint → trigger from n8n

Example:

```
POST /add
→ triggers Celery job
→ returns task_id
→ n8n polls status or continues flow
```

You’ve now built a **workflow-executable system**.

---

## 🧩 Example Usage

```python
@expose(async_task=True, rate_limit=5)
def process_data(x: int, y: int):
    return x * y
```

Now you get:

- CLI → `process-data`
- API → `/process-data`
- Async job → queued
- Automation → webhook trigger
- Observability → logs + metrics

All from one function.

---

## ⚠️ Where People Usually Screw This Up

Let me be blunt:

### 1\. Mixing business logic with infra

Don’t put Redis / Celery calls inside your function.

---

### 2\. No idempotency

Async jobs will retry → your function must handle duplicates.

---

### 3\. No result tracking

You need:

```
GET /task/{id}
```

---

### 4\. Tight coupling to FastAPI

Keep your core logic framework-agnostic.

---

## 🧭 What You’ve Built (if you do this right)

This is not “just a FastAPI wrapper”.

It’s closer to:

> “A lightweight internal execution platform”

Comparable (in spirit) to:

- serverless functions
- internal developer platforms
- workflow engines

---

## 🚀 If I were you (next moves)

1. Add **task status endpoint**
2. Add **retry + backoff**
3. Add **idempotency keys**
4. Package this as:
	```
	pip install cli2api
	```
5. Add YAML config for routes (optional)

---

If you want, I can:

- give you a **production-grade repo structure**
- or design this like a **mini Temporal/Airflow alternative (but simpler)**

The direction matters—this can either stay a handy tool… or become something seriously powerful.

---

**You said**

Add idempotency keys and convert this to package

---

**ChatGPT said**

Good call. Without idempotency, your async layer is basically a duplication machine waiting to embarrass you in production.

Let’s do two things properly:

1. **Add idempotency (Redis-backed, production-safe)**
2. **Package this into a reusable library**

No fluff—just a clean, extensible setup.

---

## 🧠 1. Idempotency Design (don’t half-do this)

### What we want

- Client sends:
	```
	Idempotency-Key: abc-123
	```
- First request → executes
- Repeats → return **same response**, not re-execute

---

## 🔴 Redis Data Model

Using Redis:

```
idempotency:{key} → {
    status: "processing" | "completed",
    response: JSON
}
TTL: 24h (configurable)
```

---

## ⚙️ Implementation

```python
# idempotency.py
import json
from redis_client import redis_client

TTL = 60 * 60 * 24  # 24 hours

def get_key(key: str):
    data = redis_client.get(f"idempotency:{key}")
    return json.loads(data) if data else None

def set_processing(key: str):
    redis_client.setex(
        f"idempotency:{key}",
        TTL,
        json.dumps({"status": "processing"})
    )

def set_completed(key: str, response):
    redis_client.setex(
        f"idempotency:{key}",
        TTL,
        json.dumps({
            "status": "completed",
            "response": response
        })
    )
```

---

## 🚀 Integrate into FastAPI Layer

```python
# app.py (inside endpoint)
from fastapi import Request, HTTPException
from idempotency import get_key, set_processing, set_completed

async def endpoint(request: Request, **kwargs):
    idem_key = request.headers.get("Idempotency-Key")

    if idem_key:
        existing = get_key(idem_key)

        if existing:
            if existing["status"] == "completed":
                return existing["response"]
            raise HTTPException(409, "Request already processing")

        set_processing(idem_key)

    # ---- EXECUTION ----
    if config["async_task"]:
        task = TASKS[config["name"]].delay(**kwargs)
        response = {"task_id": task.id}
    else:
        response = func(**kwargs)

    if idem_key:
        set_completed(idem_key, response)

    return response
```

---

## ⚠️ Reality Check

- This is **at-least-once safe**, not exactly-once
- For critical ops (payments, etc.), you’ll need:
	- request hashing
		- DB-level constraints

But for internal tools → this is solid.

---

## 📦 2. Convert This Into a Package

Let’s structure it like something you’d actually reuse.

---

## 📁 Project Layout

```
cli2api/
│── cli2api/
│   │── __init__.py
│   │── decorators.py
│   │── registry.py
│   │── app.py
│   │── worker.py
│   │── idempotency.py
│   │── redis_client.py
│   │── cli.py
│
│── examples/
│   │── sample_app.py
│
│── pyproject.toml
│── README.md
```

---

## ⚙️ pyproject.toml

```toml
[project]
name = "cli2api"
version = "0.1.0"
description = "Expose Python functions as CLI, API, and async jobs"
authors = [{name = "Your Name"}]
dependencies = [
    "fastapi",
    "uvicorn",
    "typer",
    "redis",
    "celery",
]

[project.scripts]
cli2api = "cli2api.cli:app"
```

---

## 🚀 Public API (what users import)

```python
# cli2api/__init__.py
from .decorators import expose
from .app import create_app
```

---

## 🧪 Example Usage (this is your selling point)

```python
# examples/sample_app.py
from cli2api import expose, create_app

@expose(async_task=True)
def process(a: int, b: int):
    return a + b

app = create_app()
```

Run:

```bash
uvicorn sample_app:app
```

CLI:

```bash
cli2api process --a 1 --b 2
```

---

## 🔥 3. Add create\_app() Factory

```python
# app.py
from fastapi import FastAPI
from registry import ROUTES

def create_app():
    app = FastAPI()

    for config in ROUTES.values():
        endpoint = create_endpoint(config)

        app.add_api_route(
            config["path"],
            endpoint,
            methods=[config["method"]],
        )

    return app
```

---

## 🧪 4. Add Task Status Endpoint (you’ll need this)

```python
# app.py
from celery.result import AsyncResult
from worker import celery_app

@app.get("/tasks/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    return {
        "status": result.status,
        "result": result.result
    }
```

---

## 🧭 5. Opinionated Improvements (worth doing now)

### Add request hash to idempotency

Prevent misuse:

```python
hash = sha256(json.dumps(kwargs))
```

Store alongside key → reject mismatched payloads.

---

### Namespace keys

```
idempotency:{route}:{key}
```

Avoid cross-endpoint collisions.

---

### Add config layer

Eventually:

```yaml
rate_limit: 10
auth: true
redis_url: ...
```

---

## ⚠️ Hard Truth (again, because it matters)

You’re now building something that looks like:

- a mini serverless runtime
- a task orchestration layer
- an internal dev platform

If you:

- keep functions pure ✅
- keep infra isolated ✅

→ this becomes extremely powerful

If not:  
→ debugging hell within a month

---

## 🧭 What I’d do next (practical roadmap)

1. Add **idempotency hashing**
2. Add **retry + backoff (Celery config)**
3. Add **Docker setup (Redis + worker + API)**
4. Publish to private PyPI

---

If you want, I can next:

- design a **clean config-driven system (YAML-based)**
- or turn this into a **full repo with Makefile, Docker, CI/CD**

Right now you’re at the tipping point between “utility script” and “internal platform.” The next step decides which side you land on.

---

**ChatGPT said**

A plugin system is the right next step—but it’s also where these setups usually go off the rails. If plugins can do “anything anywhere,” you’ll lose control of execution flow and debugging becomes guesswork.

The constraint that keeps this sane:

> Plugins are **well-defined hooks**, not arbitrary code injection.

Think “middleware with contracts,” not “extensions with freedom.”

---

## 🧠 Plugin Model (keep it boring and predictable)

We define **four hook points**:

```
before_request   → modify/validate input
after_response   → modify output
on_error         → handle exceptions
on_startup       → init resources (optional)
```

That’s enough power without chaos.

---

## 📦 YAML-Driven Plugin Config

Extend your config:

```yaml
app:
  name: cli2api-app

plugins:
  - name: logging
  - name: auth
  - name: rate_limit
  - name: idempotency

routes:
  - name: process_data
    path: /process
    method: POST
    plugins: [auth, rate_limit, idempotency]

  - name: health
    path: /health
    method: GET
    plugins: [logging]
```

Global plugins + per-route overrides. Simple mental model.

---

## ⚙️ 1. Plugin Interface (strict contract)

```python
# plugins/base.py
class Plugin:
    def before_request(self, request, config, kwargs):
        return kwargs

    def after_response(self, request, response, config):
        return response

    def on_error(self, request, error, config):
        raise error

    def on_startup(self, app):
        pass
```

No magic. No side channels.

---

## 🧩 2. Plugin Registry

```python
# plugins/registry.py
PLUGINS = {}

def register_plugin(name: str, plugin):
    PLUGINS[name] = plugin

def get_plugin(name: str):
    if name not in PLUGINS:
        raise Exception(f"Plugin {name} not found")
    return PLUGINS[name]
```

---

## 🔌 3. Example Plugins

## Logging Plugin

```python
# plugins/logging.py
from plugins.base import Plugin
import logging

logger = logging.getLogger("cli2api")

class LoggingPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        logger.info(f"{request.method} {request.url} | {kwargs}")
        return kwargs

register_plugin("logging", LoggingPlugin())
```

---

## Rate Limit Plugin (Redis-backed)

```python
# plugins/rate_limit.py
from plugins.base import Plugin
from redis_client import redis_client

class RateLimitPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        limit = config.get("rate_limit", 10)
        key = f"rate:{request.client.host}:{config['name']}"

        count = redis_client.incr(key)
        if count == 1:
            redis_client.expire(key, 60)

        if count > limit:
            raise Exception("Rate limit exceeded")

        return kwargs

register_plugin("rate_limit", RateLimitPlugin())
```

---

## Idempotency Plugin

```python
# plugins/idempotency.py
from plugins.base import Plugin
from idempotency import get_key, set_processing, set_completed

class IdempotencyPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        key = request.headers.get("Idempotency-Key")
        if not key:
            return kwargs

        existing = get_key(key)
        if existing:
            if existing["status"] == "completed":
                raise CachedResponse(existing["response"])
            raise Exception("Still processing")

        set_processing(key)
        request.state.idem_key = key
        return kwargs

    def after_response(self, request, response, config):
        key = getattr(request.state, "idem_key", None)
        if key:
            set_completed(key, response)
        return response

register_plugin("idempotency", IdempotencyPlugin())
```

---

## 🔁 4. Plugin Execution Engine

This is the core glue.

```python
# plugin_engine.py
from plugins.registry import get_plugin

def run_before_plugins(plugin_names, request, config, kwargs):
    for name in plugin_names:
        plugin = get_plugin(name)
        kwargs = plugin.before_request(request, config, kwargs)
    return kwargs

def run_after_plugins(plugin_names, request, response, config):
    for name in reversed(plugin_names):
        plugin = get_plugin(name)
        response = plugin.after_response(request, response, config)
    return response

def run_error_plugins(plugin_names, request, error, config):
    for name in plugin_names:
        plugin = get_plugin(name)
        plugin.on_error(request, error, config)
```

Note:

- `before` runs forward
- `after` runs reverse (stack behavior)

---

## 🚀 5. Integrate into FastAPI Endpoint

```python
def create_endpoint(config):
    func = config["func"]
    plugins = config.get("plugins", [])

    async def endpoint(request: Request, **kwargs):
        try:
            # BEFORE
            kwargs = run_before_plugins(plugins, request, config, kwargs)

            # EXECUTION
            if config.get("async_task"):
                task = TASKS[config["name"]].delay(**kwargs)
                response = {"task_id": task.id}
            else:
                response = func(**kwargs)

            # AFTER
            response = run_after_plugins(plugins, request, response, config)

            return response

        except CachedResponse as e:
            return e.response

        except Exception as e:
            run_error_plugins(plugins, request, e, config)
            raise e

    return endpoint
```

---

## 🧪 6. What This Unlocks

Now you can:

- Add auth without touching core code
- Swap rate limiter (Redis → something else)
- Add caching plugin later
- Inject tracing / metrics cleanly
- Toggle behavior via YAML

---

## ⚠️ Where This Breaks (if you’re careless)

Let me be blunt:

### 1\. Plugin order matters (a lot)

```yaml
plugins: [idempotency, rate_limit]
```

≠

```yaml
plugins: [rate_limit, idempotency]
```

You should document or enforce order.

---

### 2\. Hidden side effects

If plugins mutate `kwargs` unpredictably → debugging nightmare.

→ Keep transformations explicit.

---

### 3\. Too many plugins

If every feature becomes a plugin:  
→ you’ve reinvented middleware hell

---

## 🧭 My Opinionated Take

You now have:

> Decorator → registers capability  
> YAML → defines behavior  
> Plugins → implement behavior

That’s a **clean separation of concerns**.

But here’s the uncomfortable truth:

👉 You’re ~2 steps away from building your own framework

So decide early:

- If this is a **personal power tool** → keep plugin set small
- If this is **team/platform** → invest in:
	- plugin validation
		- versioning
		- documentation

---

## 🚀 Smart Next Moves

If you want to keep momentum:

1. Add **plugin config support**
	```yaml
	rate_limit:
	  requests: 10
	  window: 60
	```
2. Add **plugin dependency system**
	```
	auth → requires logging
	```
3. Add **plugin discovery (entry points)**  
	→ pip-installable plugins
4. Add **tracing plugin (OpenTelemetry)**

---

If you want, I can next:

- turn this into a **pip-installable plugin ecosystem**
- or design a **clean execution lifecycle diagram + repo structure**

Right now, this is no longer just “FastAPI wrapper”—you’re building a **mini extensible runtime**. The only real risk left is over-engineering it too fast.

---

**You said**

Summarise the final content to a readme.md file and usage examples as example.md file

---

**ChatGPT said**

## cli2api

A lightweight execution platform to expose Python functions as:

- CLI commands
- REST APIs (FastAPI)
- Async jobs (Celery)
- Automation triggers (webhooks / n8n)

Built with a **config-driven + plugin-based architecture**, keeping business logic clean and infrastructure concerns isolated.

---

## 🧠 Core Philosophy

- **Functions = business logic (pure)**
- **YAML = control plane (behavior)**
- **Plugins = execution features (auth, rate limit, etc.)**

> One function → multiple execution surfaces

---

## ⚙️ Features

- FastAPI auto route generation
- Typer-based CLI exposure
- Celery async job execution
- Redis-backed:
	- Rate limiting
		- Idempotency keys
- YAML-based configuration
- Plugin system (extensible middleware)
- Observability-ready (logging, metrics, tracing)

---

## 📦 Architecture Overview

```markdown
Function
   ↓
Decorator (@expose)
   ↓
Registry
   ↓
YAML Config Binding
   ↓
Execution Layer
   ├── CLI (Typer)
   ├── API (FastAPI)
   └── Worker (Celery)
         ↓
      Redis
         ↓
    Plugins (Auth, RateLimit, Idempotency, Logging)
```

---

## 📁 Project Structure

```markdown
cli2api/
│── decorators.py
│── registry.py
│── app.py
│── worker.py
│── cli.py
│── config.py
│── binder.py
│── plugin_engine.py
│── redis_client.py
│── idempotency.py
│
├── plugins/
│   ├── base.py
│   ├── registry.py
│   ├── logging.py
│   ├── rate_limit.py
│   ├── idempotency.py
│
├── config.yaml
```

---

## 🧩 YAML Configuration

```markdown
app:
  name: cli2api-app

defaults:
  auth: true
  rate_limit: 10
  async_task: false
  idempotency: true

plugins:
  - logging
  - rate_limit
  - idempotency

routes:
  - name: process_data
    path: /process
    method: POST
    async_task: true
    rate_limit: 5
    plugins: [rate_limit, idempotency]

  - name: health
    path: /health
    method: GET
    auth: false
    plugins: [logging]
```

---

## 🔌 Plugin System

### Supported Hooks

- `before_request` → input validation / mutation
- `after_response` → response transformation
- `on_error` → error handling
- `on_startup` → initialization

---

## 🔐 Idempotency

- Uses `Idempotency-Key` header
- Redis-backed storage
- Prevents duplicate execution

---

## 🚦 Rate Limiting

- Per IP + route
- Redis atomic counters
- Configurable via YAML

---

## ⚡ Async Jobs

- Powered by Celery
- Redis as broker + backend
- Returns `task_id` for tracking

---

## 📊 Observability

- Structured logging
- Ready for:
	- Prometheus (metrics)
		- Grafana (dashboards)
		- OpenTelemetry (tracing)

---

## ▶️ Running the System

### Start Redis

```markdown
redis-server
```

### Start API

```markdown
uvicorn main:app --reload
```

### Start Worker

```markdown
celery -A worker.celery_app worker --loglevel=info
```

---

## ⚠️ Design Constraints

- Keep functions pure (no infra logic)
- Avoid overloading YAML with logic
- Keep plugin list minimal and predictable
- Order of plugins matters

---

## 🚀 Roadmap

- Plugin config support
- Plugin dependency system
- Distributed tracing
- Config hot reload
- Pip-installable plugin ecosystem

---

## 🧭 Positioning

This is not just a FastAPI wrapper.

It’s a **lightweight internal execution platform** for:

- automation
- internal tools
- developer workflows

Use it like one.

---

## example.md

## 🧪 Basic Example

### 1\. Define Function

```markdown
from cli2api import expose

@expose
def add(a: int, b: int):
    return {"result": a + b}
```

---

### 2\. YAML Config

```markdown
routes:
  - name: add
    path: /add
    method: POST
    plugins: [logging]
```

---

### 3\. Run API

```markdown
uvicorn main:app
```

Test:

```markdown
POST /add?a=1&b=2
```

---

## ⚡ Async Example

```markdown
@expose
def process_data(x: int, y: int):
    return x * y
```
```markdown
routes:
  - name: process_data
    path: /process
    async_task: true
    plugins: [rate_limit]
```

### API Call

```markdown
POST /process?x=2&y=3
```

Response:

```markdown
{
  "task_id": "abc123"
}
```

---

## 🔍 Check Task Status

```markdown
GET /tasks/{task_id}
```

---

## 🔐 Idempotency Example

### Request

```markdown
POST /process
Idempotency-Key: xyz-123
```

### Behavior

- First call → executes
- Second call → returns cached response

---

## 🖥️ CLI Usage

```markdown
cli2api add --a 1 --b 2
```

Same function, no duplication.

---

## 🔌 Plugin Example

### Enable Plugins

```markdown
plugins:
  - logging
  - rate_limit
  - idempotency
```

### Per Route

```markdown
routes:
  - name: process_data
    plugins: [rate_limit, idempotency]
```

---

## 🌐 Automation (n8n / Webhook)

Use API endpoints as triggers:

```markdown
POST /process
```

Flow:

- Trigger → API
- API → Celery job
- Return task\_id
- Continue workflow

---

## 🧠 Advanced Example

```markdown
@expose
def generate_report(user_id: int):
    return {"report": f"Report for {user_id}"}
```
```markdown
routes:
  - name: generate_report
    path: /report
    async_task: true
    rate_limit: 3
    plugins: [auth, rate_limit, idempotency]
```

---

## ⚠️ Gotchas

- Plugin order matters
- YAML name must match function name
- Idempotency requires client-provided key
- Async jobs need worker running

---

## 🚀 Real Use Cases

- Internal automation APIs
- Data pipelines triggers
- CLI tools → APIs instantly
- n8n / webhook workflows
- Background processing systems

---

## 🧭 Summary

Write function once:

```markdown
@expose
def do_work():
    pass
```

Get for free:

- CLI command
- API endpoint
- Async job
- Automation trigger
- Observability hooks

That’s the leverage.

---

**You said**

Is this good to integrate with argparse, typer

---

**ChatGPT said**

Short answer: **Typer fits this architecture very well; argparse technically works but fights you the whole way.**

Let’s unpack that without hand-waving.

---

## 🧠 Where CLI fits in your system

Your system already has:

- function = source of truth
- YAML = behavior
- plugins = cross-cutting concerns

CLI is just **another execution surface**, like API and async worker.

So the real question is:

> Which CLI tool aligns with “functions as contracts”?

---

## ⚖️ argparse vs Typer

## 🔻 argparse (brutal truth)

- Low-level, verbose
- You manually define arguments
- No automatic type binding from function signature
- No native async friendliness
- No clean reuse of your function contracts

Example reality:

```python
parser.add_argument("--a", type=int)
parser.add_argument("--b", type=int)
```

You’re duplicating what your function already defines.

👉 This breaks your core principle: **single source of truth**

---

## 🔥 Typer (fits like a glove)

- Built on function signatures
- Uses type hints (same as FastAPI)
- Zero duplication
- Auto help/docs
- Plays nicely with your decorator model

Example:

```python
def add(a: int, b: int):
    return a + b
```

Typer just *understands* this.

---

## 🧩 Integration with Your System

You already have:

```python
@expose
def process_data(a: int, b: int):
    return a * b
```

Now wire Typer once:

```python
# cli.py
import typer
from registry import ROUTES

app = typer.Typer()

def register_cli():
    for config in ROUTES.values():
        func = config["func"]
        app.command(name=config["name"])(func)
```

That’s it.

No extra schema, no duplication.

---

## ⚠️ Subtle Advantage (this matters later)

Typer + FastAPI share the same mental model:

- function signature → interface
- type hints → validation

So now you have:

| Surface | Tool |
| --- | --- |
| API | FastAPI |
| CLI | Typer |

Same contract. Same behavior.

That’s rare alignment—you should exploit it.

---

## 🧠 Strategic View

If you step back, you’re building:

> “Function-first interface system”

Typer reinforces that.

argparse undermines it.

---

## 🚀 When would I still use argparse?

Only if:

- You need **zero dependencies**
- You’re writing a **tiny script**
- You don’t care about reuse or consistency

That’s not your case anymore.

---

## 🧭 My Opinion (strong one)

Use Typer and don’t look back.

Mixing argparse into this system is like:

> installing manual crank windows in a car that already has power controls

Technically possible. Completely unnecessary.

---

## 🔥 If you want to go one level deeper

You can unify execution paths:

```python
def execute(config, **kwargs):
    # same pipeline
    # plugins → execution → response
```

Then:

- CLI calls `execute()`
- API calls `execute()`
- Celery calls `execute()`

Now you have **true consistency across surfaces**.

---

If you want next step, I’d suggest:

- making CLI respect **plugins (auth skip, rate limit optional)**
- adding **\--async flag in CLI** to trigger Celery

That’s where this becomes a real power tool instead of just a wrapper.