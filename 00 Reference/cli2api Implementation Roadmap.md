
# Steps to Implement

> See also: [[cli2api System Architecture]] | [[cli2api Feature Roadmap and Enhancements]] | [[10 Examples of Use]]

## Phase 1: Core Foundation

### Step 1.1 — Registry + Decorator

Goal: Functions can be registered via a decorator.

Files: `registry.py`, `decorators.py`

- `ROUTES` dict in registry.py
- `register_route(path, func)` stores function
- `expose_api(path)` decorator calls register_route
- Keep it thin — no logic, just registration

### Step 1.2 — FastAPI App

Goal: Registered functions auto-generate REST endpoints.

Files: `app.py`

- `create_endpoint(func)` wraps function in async endpoint
- `register_routes(app)` iterates ROUTES and calls `app.add_api_route`
- Handles both sync and async functions via `inspect.iscoroutinefunction`

### Step 1.3 — Example CLI Functions

Goal: Demonstrate decorator usage.

File: `cli.py`

- Define 2-3 example functions with `@expose_api`
- Show typed parameters (auto validation via FastAPI)

### Step 1.4 — Entry Point

Goal: Run the API server.

File: `main.py`

- Import cli (triggers registration)
- `uvicorn.run(app)`

**Checkpoint**: `python main.py` starts server, `/docs` shows auto-generated API.

---

## Phase 2: Enhanced Decorator + Built-in Features

### Step 2.1 — Decorator with Metadata

Goal: Decorator carries config, not just path.

File: `decorators.py`

- `expose_api(path, method, auth, rate_limit)` signature
- Auto-derive path from function name if not provided: `add_numbers -> /add-numbers`
- Store structured config dict in registry

### Step 2.2 — Registry Stores Structured Config

Goal: Registry values are dicts, not just callables.

File: `registry.py`

- `register_route(path, config: dict)` where config = {func, method, auth, rate_limit}

### Step 2.3 — Auth Middleware

Goal: API key validation per route.

File: `app.py`

- `verify_api_key(request)` checks `x-api-key` header against configured keys
- `check_rate_limit(path, limit, request)` in-memory (dev only)
- Endpoint factory applies auth + rate limit based on config

### Step 2.4 — Input Validation

Goal: Pydantic models from function signatures.

- FastAPI handles this automatically from type hints
- Optional: explicit Pydantic models for complex inputs

### Step 2.5 — Logging

Goal: Request/response logging.

- `print` statements for now (upgrade to structured logging later)
- Log method, path, params on each request

**Checkpoint**: API has auth, rate limiting, input validation, and logging.

---

## Phase 3: CLI Dual Mode + Packaging

### Step 3.1 — Typer Integration

> Also see: [[Integration - Typer]]

Goal: Same function exposed as CLI command.

File: `cli_app.py`

- `typer.Typer()` app
- `register_cli()` iterates ROUTES, registers each as `app.command()(func)`
- CLI args derived from function signature (zero duplication)

### Step 3.2 — Unified Decorator

Goal: Single decorator registers both API and CLI.

File: `decorators.py`

- `expose(path, method, auth, rate_limit, async_task)` calls:
  - `register_route(config)` for API
  - `register_cli(config)` for CLI
  - `register_task(config)` for async (Phase 4)

### Step 3.3 — Package Structure

Goal: Convert to pip-installable package.

Files: `pyproject.toml`, `cli2api/__init__.py`

- `pyproject.toml` with dependencies: fastapi, uvicorn, typer, redis, celery
- `[project.scripts] cli2api = "cli2api.cli:app"` for CLI entry point
- `__init__.py` exports `expose` and `create_app`

### Step 3.4 — create_app() Factory

Goal: App creation is programmatic, not module-side-effect.

File: `app.py`

- `create_app()` builds FastAPI, applies config, registers routes
- Task status endpoint: `GET /tasks/{task_id}`

**Checkpoint**: `pip install -e .` works, `cli2api --help` shows commands.

---

## Phase 4: Async Jobs + Redis

### Step 4.1 — Redis Client

Goal: Redis connection available.

File: `redis_client.py`

- `redis.Redis(host, port, db)` connection

### Step 4.2 — Celery Worker

Goal: Async task execution.

File: `worker.py`

- `Celery("worker", broker="redis://localhost:6379")`
- `@celery_app.task(name=name)` wrapper per function
- `TASKS` dict maps name -> celery task

### Step 4.3 — Redis-backed Rate Limiting

Goal: Production-safe rate limiting (replace in-memory).

File: `app.py` (update rate limit function)

- Atomic `INCR` + `EXPIRE` in Redis
- Per IP + route key: `rate:{client_ip}:{path}`

### Step 4.4 — Idempotency

Goal: Prevent duplicate execution of async jobs.

File: `idempotency.py`

- Redis data model: `idempotency:{key} -> {status, response}` with 24h TTL
- `get_key()`, `set_processing()`, `set_completed()` functions
- Integrate into FastAPI endpoint: check key before execution, store result after

### Step 4.5 — Async Execution in API

Goal: `async_task=True` routes trigger Celery.

File: `app.py` (update endpoint factory)

- If `config["async_task"]`: `TASKS[name].delay(**kwargs)`, return `{"task_id": task.id}`
- Task status endpoint: `GET /tasks/{task_id}` returns `{status, result}`

**Checkpoint**: Async jobs run via Celery, rate limiting uses Redis, idempotency prevents duplicates.

---

## Phase 5: YAML-Driven Configuration

### Step 5.1 — Config Loader

Goal: Load YAML configuration.

File: `config.py`

- `Config` class reads `config.yaml` via `yaml.safe_load`
- Exposes `defaults` and `routes` attributes

### Step 5.2 — Binder

Goal: Map YAML route names to registered functions.

File: `binder.py`

- `apply_config()` iterates YAML routes, merges defaults, updates ROUTES dict
- Raises if YAML references unregistered function

### Step 5.3 — Minimal Decorator

Goal: Decorator is pure registration, no config.

File: `decorators.py` (update)

- `expose(func)` — just registers name + func
- All config (path, method, rate_limit, plugins) comes from YAML

### Step 5.4 — App Factory with YAML

Goal: create_app applies YAML config before registering routes.

File: `app.py` (update)

- `create_app()` calls `apply_config()` first
- Routes read merged config from ROUTES dict

### Step 5.5 — Config Validation

Goal: Catch misconfig at startup.

File: `config.py` or `binder.py`

- Pydantic model `RouteConfig(name, path, method, auth, rate_limit, async_task)`
- Validate YAML structure before applying

**Checkpoint**: All route behavior controlled by YAML, decorator is minimal.

---

## Phase 6: Plugin System

### Step 6.1 — Plugin Base Class

Goal: Define strict plugin interface.

File: `plugins/base.py`

- `Plugin` class with 4 hooks: before_request, after_response, on_error, on_startup
- All hooks have no-op defaults

### Step 6.2 — Plugin Registry

Goal: Register and retrieve plugins by name.

File: `plugins/registry.py`

- `PLUGINS` dict + `register_plugin(name, plugin)` + `get_plugin(name)`

### Step 6.3 — Plugin Execution Engine

Goal: Run plugins in order during endpoint execution.

File: `plugin_engine.py`

- `run_before_plugins(names, request, config, kwargs)` — forward order
- `run_after_plugins(names, request, response, config)` — reverse order
- `run_error_plugins(names, request, error, config)` — forward order

### Step 6.4 — YAML Plugin Config

Goal: Configure plugins per route and globally.

File: `config.yaml` (update)

- `plugins: [logging, rate_limit]` at app level
- `plugins: [auth, rate_limit]` per route

### Step 6.5 — Example Plugins

> Also see: [[Plugin System]]

Goal: Implement core plugins.

Files: `plugins/logging.py`, `plugins/rate_limit.py`, `plugins/idempotency.py`, `plugins/auth.py`

- Logging: log request method, url, params
- Rate Limit: Redis atomic counter per IP + route
- Idempotency: check/store idempotency key
- Auth: validate x-api-key header

**Checkpoint**: Plugins are extensible hooks, configured via YAML, executed in order.

---

## Phase 7: Production Hardening

### Step 7.1 — Structured Logging

Goal: JSON logs for ELK / structured log aggregation.

- Replace `print` with `logging.getLogger("cli2api")`
- Log format: `{"event": "api_call", "route": "...", "params": ...}`

### Step 7.2 — Observability

Goal: Metrics and tracing.

- Prometheus metrics endpoint
- OpenTelemetry tracing hooks
- Grafana dashboard (config)

### Step 7.3 — Environment-based Configs

Goal: Different configs per environment.

- `config.dev.yaml`, `config.prod.yaml`
- Load based on `ENV` environment variable

### Step 7.4 — Docker Setup

Goal: One-command startup.

- `docker-compose.yml` with Redis, API, Worker services
- Dockerfile for the app

### Step 7.5 — Retry + Backoff

Goal: Celery task retry on failure.

- `@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)`
- Exponential backoff config

### Step 7.6 — Hot Reload

Goal: Config changes without restart.

- Watch YAML file for changes
- Re-apply binder without restarting server

**Checkpoint**: Production-ready with Docker, observability, retry, and hot reload.


```yaml
title: cli2api Implementation Roadmap

folder: Projects/cli2api/Implementation

categorical:
  domain:
    value: software-engineering
    reason: Describes the phased implementation plan for building a reusable developer platform.

  subdomain: framework-implementation

  note_type:
    value: project
    reason: Defines implementation phases, milestones, checkpoints, and deliverables for the project.

  source_type:
    value: self
    reason: Self-authored engineering roadmap.

  status:
    value: curated
    reason: Well-structured implementation plan with stable milestones and execution order.

  level:
    value: advanced
    reason: Covers framework development, API generation, plugin architecture, asynchronous processing, packaging, and production readiness.

ratings:
  confidence:
    score: 5
    reason: Self-authored roadmap without external claims.

  completeness:
    score: 5
    reason: Covers implementation from MVP through production hardening, including checkpoints, technologies, and file-level responsibilities.

  complexity:
    score: 5
    reason: Involves framework architecture, code generation, plugin execution, asynchronous processing, packaging, and deployment concerns.

  importance:
    score: 5
    reason: Serves as the execution blueprint for the entire cli2api project.

  career_relevance:
    score: 5
    reason: Demonstrates framework engineering, software architecture, developer tooling, and platform design skills relevant to senior engineering roles.

  freshness:
    score: 5
    reason: Incorporates modern Python ecosystem practices including FastAPI, Typer, Celery, Redis, YAML configuration, plugin systems, and observability.

  reusability:
    score: 5
    reason: The phased implementation strategy can be reused when building similar frameworks or internal developer platforms.

  review_priority:
    score: 4
    reason: Active implementation roadmap that should evolve as phases are completed and architectural decisions change.

  connectedness:
    score: 5
    reason: Links to architecture, goals, plugins, examples, integrations, ADRs, and individual implementation notes across the project.

  actionability:
    score: 5
    reason: Breaks the project into concrete, sequential implementation steps with measurable checkpoints after each phase.

  quality_score:
    score: 99
    reason: Comprehensive engineering roadmap with clear sequencing, incremental milestones, implementation boundaries, and production evolution.

custom:
  tags:
    - cli2api
    - implementation
    - framework
    - roadmap
    - developer-platform

ai_summary: >
  Defines the complete implementation roadmap for cli2api across seven incremental phases. The roadmap progresses from a minimal FastAPI-based function registry to a production-ready execution platform supporting CLI commands, REST APIs, asynchronous Celery workers, declarative YAML configuration, extensible plugins, Redis-backed infrastructure, and production features such as observability, Docker deployment, retries, and hot reload. Each phase includes implementation tasks, file responsibilities, and checkpoints, providing a structured path from MVP to a mature internal developer platform.
```

### Why this classification?

This note is different from your other `cli2api` notes:

- **`01 Goal`** → explains **why** the project exists.
    
- **`02 Architecture`** → explains **how the system is designed**.
    
- **This note (`03 Steps to Implement`)** → explains **how to build it**, step by step.
    

That's why I classified it as a **`project`** rather than an **`architecture`** note. It's an execution plan, not a description of the architecture itself.

I also think your `cli2api` project is naturally converging on this structure:

```text
Projects/
└── cli2api/
    ├── 00 README.md                ← Project hub
    ├── 01 Goal.md                  ← Vision
    ├── 02 Architecture.md          ← System design
    ├── 03 Implementation.md        ← This note
    ├── 04 Enhancements.md
    ├── 05 Plugins.md
    ├── 06 Configuration.md
    ├── 07 Typer Integration.md
    ├── ADR/
    ├── Architecture/
    ├── Concepts/
    └── Tasks/
```

This separation gives each note a single responsibility and makes the knowledge graph much cleaner.