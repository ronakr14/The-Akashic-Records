```table-of-contents
```

# Examples of Use

> See also: [[04 Enhancements Included]] | [[05 Plugins That Can Be Added]] | [[07 Integration with Typer]] | [[09 Integration with Rich]]

## Example 1: Basic — Hello World

The simplest possible usage. Define a function, expose it as API and CLI.

```python
# app.py
from cli2api import expose, create_app

@expose
def hello(name: str = "world"):
    return {"message": f"Hello {name}"}

app = create_app()
```

```bash
# Run API
uvicorn app:app --reload

# Test API
curl "http://localhost:8000/hello?name=Ronak"
# {"message":"Hello Ronak"}

# Test CLI
cli2api hello --name Ronak
# {"message":"Hello Ronak"}
```

---

## Example 2: Math Operations

Multiple functions with typed parameters.

```python
# app.py
from cli2api import expose, create_app

@expose
def add(a: int, b: int):
    return {"result": a + b}

@expose
def multiply(a: int, b: int):
    return {"result": a * b}

@expose
def divide(a: float, b: float):
    if b == 0:
        return {"error": "Division by zero"}
    return {"result": a / b}

app = create_app()
```

```bash
# API
curl "http://localhost:8000/add?a=1&b=2"
# {"result":3}

curl "http://localhost:8000/multiply?a=3&b=4"
# {"result":12}

# CLI
cli2api add --a 1 --b 2
# {"result":3}

cli2api multiply --a 3 --b 4
# {"result":12}
```

---

## Example 3: YAML-Driven Configuration

Move all config to YAML. Decorator becomes minimal.

```python
# app.py
from cli2api import expose, create_app

@expose
def process_data(x: int, y: int):
    return x * y

@expose
def health():
    return {"status": "ok"}

app = create_app()
```

```yaml
# config.yaml
app:
  name: my-app
  version: "1.0"

defaults:
  auth: true
  rate_limit: 10

routes:
  - name: process_data
    path: /process
    method: POST
    rate_limit: 5
    plugins: [rate_limit, logging]

  - name: health
    path: /health
    method: GET
    auth: false
    plugins: [logging]
```

```bash
# API
curl -X POST "http://localhost:8000/process?x=2&y=3" -H "x-api-key: secret123"
# 6

curl "http://localhost:8000/health"
# {"status":"ok"}
```

---

## Example 4: Async Job with Celery

Long-running task executed in background.

```python
# app.py
from cli2api import expose, create_app

@expose
def generate_report(user_id: int):
    # Simulate heavy computation
    import time
    time.sleep(30)
    return {"report": f"Report for user {user_id}", "records": 1500}

app = create_app()
```

```yaml
# config.yaml
routes:
  - name: generate_report
    path: /report
    method: POST
    async_task: true
    rate_limit: 3
    plugins: [auth, rate_limit, idempotency]
```

```bash
# Start worker (in another terminal)
celery -A worker.celery_app worker --loglevel=info

# API call
curl -X POST "http://localhost:8000/report?user_id=42" -H "x-api-key: secret123"
# {"task_id":"abc-123-def"}

# Check status
curl "http://localhost:8000/tasks/abc-123-def"
# {"status":"completed","result":{"report":"Report for user 42","records":1500}}
```

---

## Example 5: Idempotency

Prevent duplicate execution with idempotency key.

```bash
# First request — executes
curl -X POST "http://localhost:8000/report?user_id=42" \
  -H "x-api-key: secret123" \
  -H "Idempotency-Key: unique-key-001"
# {"task_id":"abc-123-def"}

# Same request again — returns cached result, no re-execution
curl -X POST "http://localhost:8000/report?user_id=42" \
  -H "x-api-key: secret123" \
  -H "Idempotency-Key: unique-key-001"
# {"task_id":"abc-123-def"}  (cached, instant response)
```

---

## Example 6: Rate Limiting

Exceeding the rate limit returns 429.

```yaml
# config.yaml
routes:
  - name: add
    path: /add
    rate_limit: 3  # Only 3 requests per minute
    plugins: [rate_limit]
```

```bash
# First 3 requests succeed
curl "http://localhost:8000/add?a=1&b=2"  # OK
curl "http://localhost:8000/add?a=3&b=4"  # OK
curl "http://localhost:8000/add?a=5&b=6"  # OK

# 4th request fails
curl "http://localhost:8000/add?a=7&b=8"
# {"detail":"Rate limit exceeded"}  (HTTP 429)
```

---

## Example 7: Auth Protection

Routes with and without authentication.

```yaml
# config.yaml
defaults:
  auth: true  # All routes require auth by default

routes:
  - name: health
    path: /health
    auth: false  # Override: no auth needed

  - name: admin_status
    path: /admin/status
    auth: true  # Explicit: requires auth
```

```bash
# Health — no auth needed
curl "http://localhost:8000/health"
# {"status":"ok"}

# Admin — requires API key
curl "http://localhost:8000/admin/status"
# {"detail":"Invalid API Key"}  (HTTP 401)

curl "http://localhost:8000/admin/status" -H "x-api-key: secret123"
# {"status":"admin_ok","db":"connected"}
```

---

## Example 8: Plugin Configuration

Configure plugins with custom settings.

```yaml
# config.yaml
app:
  name: my-app

plugins:
  - name: rate_limit
    config:
      requests: 10
      window: 60
  - name: auth
    config:
      roles: ["admin", "operator"]

routes:
  - name: process
    path: /process
    plugins: [auth, rate_limit, idempotency]
```

---

## Example 9: Rich CLI Output

Beautiful terminal output with Rich.

```bash
# Table output for list data
cli2api list-users --rich
# ┏━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓
# ┃ ID ┃ Name   ┃ Role     ┃ Last Login  ┃
# ┡━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩
# │ 1  │ Alice  │ admin    │ 2026-06-22 │
# │ 2  │ Bob    │ operator │ 2026-06-21 │
# │ 3  │ Carol  │ viewer   │ 2026-06-20 │
# └────┴────────┴──────────┴────────────┘

# JSON output
cli2api get-user --id 1 --format json
# {
#   "id": 1,
#   "name": "Alice",
#   "role": "admin",
#   "last_login": "2026-06-22T10:30:00"
# }

# Progress bar for long tasks
cli2api generate-report --user-id 42
# ⠹ Waiting for task abc-123-def...
```

---

## Example 10: n8n / Webhook Integration

Use API endpoints as workflow triggers.

```yaml
# config.yaml
routes:
  - name: trigger_pipeline
    path: /pipeline/trigger
    method: POST
    async_task: true
    plugins: [auth, idempotency]
```

```python
# app.py
@expose
def trigger_pipeline(pipeline_name: str, params: str = "{}"):
    """Trigger a data pipeline."""
    return {"initiated": True, "pipeline": pipeline_name}

# n8n workflow:
# 1. Webhook node: POST /pipeline/trigger?pipeline_name=daily_sync
# 2. Wait node: 5 seconds
# 3. HTTP node: GET /tasks/{task_id} (poll until completed)
# 4. If completed -> continue; else -> wait again
```

---

## Example 11: Minimal Package Usage

Using cli2api as an installed package.

```bash
# Install
pip install cli2api

# Create your app
cat > myapp.py << 'EOF'
from cli2api import expose, create_app

@expose
def greet(name: str):
    return {"greeting": f"Hi {name}!"}

@expose
def status():
    return {"status": "running", "version": "1.0.0"}

app = create_app()
EOF

# Run
uvicorn myapp:app

# CLI
cli2api greet --name Ronak
cli2api status
```

---

## Example 12: Environment-Based Configs

Different behavior per environment.

```bash
# Development
ENV=development uvicorn app:app
# Loads config.dev.yaml (auth=false, rate_limit=100)

# Production
ENV=production uvicorn app:app
# Loads config.prod.yaml (auth=true, rate_limit=10)
```

```yaml
# config.dev.yaml
defaults:
  auth: false
  rate_limit: 100

# config.prod.yaml
defaults:
  auth: true
  rate_limit: 10
  redis_url: "redis://prod-redis:6379/0"
```

---

## Example 13: Custom Plugin

Writing your own plugin.

```python
# plugins/timestamp.py
from plugins.base import Plugin
from datetime import datetime

class TimestampPlugin(Plugin):
    def after_response(self, request, response, config):
        if isinstance(response, dict):
            response["timestamp"] = datetime.utcnow().isoformat()
        return response

# Register
from plugins.registry import register_plugin
register_plugin("timestamp", TimestampPlugin())
```

```yaml
# config.yaml
routes:
  - name: get_time
    path: /time
    plugins: [timestamp]
```

```bash
curl "http://localhost:8000/time"
# {"timestamp":"2026-06-23T14:30:00"}
```

---

## Example 14: Full Production Setup

Docker + Redis + Celery + API.

```yaml
# docker-compose.yml
version: "3.8"
services:
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  api:
    build: .
    command: uvicorn app:app --host 0.0.0.0 --port 8000
    ports: ["8000:8000"]
    depends_on: [redis]
    environment:
      - REDIS_URL=redis://redis:6379/0

  worker:
    build: .
    command: celery -A worker.celery_app worker --loglevel=info
    depends_on: [redis]
    environment:
      - REDIS_URL=redis://redis:6379/0
```

```bash
# Start everything
docker-compose up

# API available at http://localhost:8000
# Worker processes background tasks
# Redis handles rate limiting + idempotency
```

---

## Summary Pattern

Every example follows the same pattern:

1. **Define** a pure function with type hints
2. **Decorate** with `@expose` (or configure via YAML)
3. **Get for free**: API endpoint + CLI command + async job + plugins

Write once. Run everywhere.
