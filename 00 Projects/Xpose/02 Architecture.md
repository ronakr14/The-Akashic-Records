---
tags:
  - cli2api
  - project
  - architecture
  - design
related:
  - "[[01 Goal]]"
  - "[[03 Steps to Implement]]"
  - "[[05 Plugins That Can Be Added]]"
  - "[[06 Constraints]]"
---

# Architecture

> See also: [[01 Goal]] | [[03 Steps to Implement]] | [[05 Plugins That Can Be Added]]

## High-Level Data Flow

```
Function (pure business logic)
   |
   v
Decorator (@expose)  -- registers function + metadata
   |
   v
Registry (central store of all registered functions)
   |
   v
YAML Config Binding  -- merges declarative policy from config.yaml
   |
   v
Execution Layer
   |-- CLI (Typer)       -- terminal invocation
   |-- API (FastAPI)     -- HTTP REST endpoints
   |-- Worker (Celery)   -- async background jobs
         |
         v
      Redis (rate limiting, idempotency, broker, caching)
         |
         v
    Plugins (Auth, RateLimit, Idempotency, Logging)
```

## Layer Responsibilities

### 1. Functions (Business Logic)

- Pure Python functions with type hints
- No framework imports (no FastAPI, Celery, Redis inside)
- Signature is the contract — drives CLI args, API params, and validation

### 2. Decorator (@expose)

- Registration layer only — no execution logic
- Stores function reference + metadata (name, path, method, auth, rate_limit, async_task)
- Later versions can be parameterless when YAML owns the config

```python
# Current: decorator carries config
@expose(path="/process", method="POST", rate_limit=5)
def process_data(x: int, y: int):
    return x * y

# Future (YAML-driven): decorator is minimal
@expose
def process_data(x: int, y: int):
    return x * y
# config.yaml owns: path, method, rate_limit, plugins, etc.
```

### 3. Registry

- Central dict: name -> config dict
- Single source of truth for all registered functions
- Read by CLI, API, and worker layers

```python
ROUTES = {
    "process_data": {
        "name": "process_data",
        "func": <function>,
        "path": "/process-data",
        "method": "POST",
        "auth": True,
        "rate_limit": 10,
        "async_task": False,
    }
}
```

### 4. YAML Config (Control Plane)

- Declarative policy: what path, what rate limit, which plugins
- Does NOT contain business logic, transformations, or conditional flows
- Merged with defaults; route-level overrides win

### 5. Binder

- Maps YAML route names to registered Python functions
- Merges defaults with per-route config
- Validates that every YAML route has a matching function

### 6. Execution Layer

Three surfaces, same function, same plugin pipeline:

| Surface | Tool | Trigger |
|---------|------|---------|
| CLI | Typer | Terminal command |
| API | FastAPI | HTTP request |
| Worker | Celery | Queue message |

All three call into the same `execute()` pipeline:
1. Run before_request plugins
2. Execute function
3. Run after_response plugins
4. Return response

### 7. Plugin Engine

Four well-defined hook points:

```
before_request   -> modify/validate input kwargs
after_response   -> modify output / format response
on_error         -> handle exceptions / fallback
on_startup       -> init resources (DB connections, caches)
```

Execution order:
- `before_request`: forward order (as listed in config)
- `after_response`: reverse order (stack unwind behavior)
- `on_error`: forward order, can suppress or transform errors

### 8. Redis

Used as:
- Rate limiter (atomic counters with TTL)
- Celery broker (task queue)
- Celery result backend (task status + results)
- Idempotency key store (key -> {status, response})
- Future: caching layer

## Project Structure

```
cli2api/
|-- cli2api/
|   |-- __init__.py       # public API: expose, create_app
|   |-- decorators.py         # @expose decorator
|   |-- registry.py           # ROUTES dict + register_route
|   |-- app.py                # FastAPI app factory + endpoint creation
|   |-- worker.py             # Celery app + task registration
|   |-- cli_app.py            # Typer CLI registration
|   |-- config.py             # YAML config loader
|   |-- binder.py             # YAML -> registry binding
|   |-- plugin_engine.py      # run_before/after/error plugins
|   |-- redis_client.py       # Redis connection
|   |-- idempotency.py        # Idempotency key management
|   |-- cli.py                # CLI entry point (typer script)
|
|   |-- plugins/
|       |-- base.py           # Plugin base class (interface contract)
|       |-- registry.py       # PLUGINS dict + register/get
|       |-- logging.py        # Request/response logging
|       |-- rate_limit.py     # Redis-backed rate limiting
|       |-- idempotency.py    # Idempotency key handling
|       |-- auth.py           # API key / JWT validation
|
|-- config.yaml               # Route + plugin configuration
|-- examples/
|   |-- sample_app.py         # Minimal usage example
|
|-- pyproject.toml            # Package metadata + dependencies
|-- README.md                 # Project overview
```

## Key Design Decisions

1. **Function signature is the single source of truth** — CLI args, API params, and validation all derive from it
2. **YAML owns policy, Python owns logic** — no business logic in config files
3. **Plugins are constrained hooks** — not arbitrary middleware injection
4. **Same execution pipeline for all surfaces** — CLI, API, and Celery all run plugins identically
5. **Redis as shared infrastructure** — rate limiting, broker, caching, idempotency all use the same Redis instance
