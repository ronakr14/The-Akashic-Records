---
type: project
tags:
  - cli2api
  - project
  - goal
  - architecture
related:
  - "[[02 Architecture]]"
  - "[[03 Steps to Implement]]"
  - "[[04 Enhancements Included]]"
  - "[[06 Constraints]]"
---

# Goal

> Back to: [[00 Projects|Xpose Project]]

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
