---
domain: Programming
domain_suggested: null
category: Snippet
category_suggested: null
source_type: obsidian
status: review
tags: [xpose, enhancements, features]
---




# Enhancements Included

> See also: [[02 Architecture]] | [[03 Steps to Implement]] | [[05 Plugins That Can Be Added]]

Beyond the basic "decorator that exposes a function as an API endpoint," cli2api includes the following enhancements to make it a production-capable internal execution platform.

## 1. Auto Route Naming

Instead of manually specifying `/add` for every function, the path is derived from the function name:

```python
def add_numbers(a: int, b: int):
    return a + b
# Auto-generates: POST /add-numbers
```

Underscores become hyphens. Override with explicit `path` in decorator or YAML.

## 2. Input Validation via Pydantic

Function type hints are automatically validated by FastAPI. For complex inputs, explicit Pydantic models can be used:

```python
class AddInput(BaseModel):
    a: int
    b: int
```

No manual validation code needed — invalid inputs return 422 with clear error messages.

## 3. API Key Security

> Also see: [[05 Plugins That Can Be Added#4. Auth Plugin]] | [[10 Examples of Use#Example 7: Auth Protection]]

Per-route API key validation via `x-api-key` header:

```python
@expose_api(auth=True)
def sensitive_operation():
    ...
```

Keys stored in env vars or DB (not in code for production). Global default + per-route override.

## 4. Rate Limiting (Redis-backed)

Per-IP + per-route rate limiting using Redis atomic counters:

- Key: `rate:{client_ip}:{route_path}`
- Atomic `INCR` + `EXPIRE` (sliding window)
- Configurable per route via YAML: `rate_limit: 10` (requests per minute)
- Returns HTTP 429 when exceeded

## 5. Async Job Queue (Celery)

> Also see: [[03 Steps to Implement#Phase 4: Async Jobs + Redis]] | [[10 Examples of Use#Example 4: Async Job with Celery]]

Mark any function as async to execute it via Celery worker:

```python
@expose(async_task=True)
def process_data(x: int, y: int):
    return x * y
```

- API returns `{"task_id": "abc123"}` immediately
- Worker processes in background
- Check status via `GET /tasks/{task_id}`
- Redis as broker + result backend

## 6. Idempotency Keys

> Also see: [[05 Plugins That Can Be Added#3. Idempotency Plugin]] | [[10 Examples of Use#Example 5: Idempotency]]

Prevent duplicate execution for critical operations:

- Client sends `Idempotency-Key: unique-key` header
- First request: executes and stores result in Redis
- Repeat request: returns cached response (no re-execution)
- Redis key TTL: 24 hours (configurable)
- At-least-once safe (not exactly-once — for payments, add DB constraints)

## 7. CLI + API Dual Mode

> Also see: [[07 Integration with Typer]] | [[08 Integration with Argparse]] | [[09 Integration with Rich]]

Same function exposed as both REST endpoint and CLI command:

- API: `POST /process-data?x=2&y=3`
- CLI: `cli2api process-data --x 2 --y 3`
- Zero duplication — same function, same validation, same behavior

## 8. YAML-Driven Configuration

Separate policy from code:

```yaml
defaults:
  auth: true
  rate_limit: 10

routes:
  - name: process_data
    path: /process
    async_task: true
    rate_limit: 5
```

Change behavior without touching Python code. Environment-specific configs: `config.dev.yaml`, `config.prod.yaml`.

## 9. Plugin System

> Also see: [[05 Plugins That Can Be Added]] | [[06 Constraints#3. Plugins are Hooks, Not Injection]]

Extensible middleware with strict contracts:

- `before_request` — modify/validate input
- `after_response` — transform output
- `on_error` — handle exceptions
- `on_startup` — initialize resources

Configure per route via YAML. Built-in plugins: logging, rate_limit, idempotency, auth.

## 10. Observability

Ready for production monitoring:

- Structured JSON logging (swap `print` for `logging.getLogger`)
- Prometheus metrics endpoint
- OpenTelemetry tracing hooks
- Grafana dashboards (config)

## 11. Packaging

Installable as a pip package:

```bash
pip install cli2api
```

CLI entry point: `cli2api --help` shows all registered commands.

## 12. Automation Integration (n8n / Webhooks)

API endpoints serve as workflow triggers:

```
n8n webhook -> POST /process-data
            -> Celery job queued
            -> Returns task_id
            -> n8n polls /tasks/{task_id}
            -> Continues workflow
```

## 13. Config Validation

Catch misconfig at startup:

- Pydantic model validates YAML structure
- Startup validation: every YAML route must have matching function
- Fail fast on typos or missing registrations

## 14. Request Hash for Idempotency

Prevent idempotency key misuse:

```python
hash = sha256(json.dumps(kwargs))
```

Store hash alongside key — reject if same key used with different payload.

## 15. Plugin Config Support

Plugins accept their own configuration:

```yaml
rate_limit:
  requests: 10
  window: 60
auth:
  roles: ["admin"]
```

## 16. Plugin Dependency System

Declare plugin ordering:

```yaml
auth:
  requires: [logging]
```

Ensures logging runs before auth check.

## 17. Plugin Discovery (Entry Points)

Pip-installable third-party plugins:

```toml
[project.entry-points."cli2api.plugins"]
my_plugin = "my_plugin_package:register"
```

## 18. Distributed Tracing

OpenTelemetry integration for debugging across:

- API request -> Celery worker -> Redis -> response
- Trace IDs propagated through all layers

## 19. Retry + Backoff

Celery tasks retry on failure:

```python
@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
```

Exponential backoff configurable per task.

## 20. Hot Reload

> Also see: [[03 Steps to Implement#Step 7.6 — Hot Reload]]

YAML config changes apply without server restart:

- File watcher on config.yaml
- Re-apply binder on change
- Zero-downtime config updates
