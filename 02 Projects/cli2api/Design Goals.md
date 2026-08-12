---
domain: software-engineering
subdomain: developer-platform
note_type: architecture
source_type: self
status: curated
level: advanced
tags:
  - cli2api
  - fastapi
  - typer
---
# AI Summary
Vision document for cli2api, a lightweight internal developer platform that exposes a single Python function as multiple execution surfaces including CLI commands, REST APIs, asynchronous jobs, and automation webhooks. The architecture separates business logic, declarative YAML configuration, and execution plugins to eliminate boilerplate while keeping functions framework-agnostic. T he note defines the project's philosophy, target use cases, non-goals, and success criteria, serving as the architectural foundation for future implementation.

---
## What is cli2api?

A lightweight execution platform to expose Python functions as multiple execution surfaces from a single definition:

- CLI commands (via Typer)
- REST APIs (via FastAPI)
- Async jobs (via Celery)
- Automation triggers (webhooks / n8n)

## Core Philosophy

- **Functions = business logic (pure, framework-agnostic)**
- **YAML = control plane (behavior, not logic)**
- **Plugins = execution features (auth, rate limit, idempotency, logging)**

One function definition should unlock all surfaces without duplicating code or schema.

## What Problem Does It Solve?

Internal tools and scripts often need to be:
1. Run from terminal (CLI)
2. Called by other services (API)
3. Executed asynchronously (background jobs)
4. Triggered by automation platforms (n8n, webhooks)

Normally this means 4 separate implementations or heavy boilerplate. cli2api lets you write the function once and configure how it's exposed.

## Target Use Cases

- Internal automation APIs
- Data pipeline triggers
- CLI tools that also need HTTP interfaces
- n8n / webhook workflow backends
- Background processing systems

## What This Is NOT

- Not a public API framework (no versioning, no public-facing error contracts)
- Not a replacement for full workflow engines (Airflow, Temporal)
- Not a general-purpose web framework

It is a **personal power tool / internal developer platform** for teams that need to expose business logic across multiple surfaces quickly and cleanly.

## Success Criteria

- Zero boilerplate per function beyond the @expose decorator
- Same function signature drives CLI, API, and async job
- Plugin system is extensible but constrained (hooks, not arbitrary injection)
- YAML config is declarative control, not logic engine
- Functions remain pure — no infra leakage into business logic
