 Goal

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

```yaml
title: cli2api Project Vision and Design Goals

folder: Projects/cli2api

categorical:
  domain:
    value: software-engineering
    reason: Defines the vision and architecture of a reusable developer platform for exposing business logic across execution interfaces.

  subdomain: developer-platform

  note_type:
    value: architecture
    reason: Captures the project's architectural philosophy, scope, design principles, and success criteria rather than implementation details.

  source_type:
    value: self
    reason: Self-authored project vision and architectural specification.

  status:
    value: curated
    reason: Well-structured, stable project definition suitable as the project's root documentation.

  level:
    value: advanced
    reason: Assumes knowledge of APIs, CLIs, asynchronous processing, plugin architectures, and software design principles.

ratings:
  confidence:
    score: 5
    reason: Self-authored architectural vision with no external claims requiring validation.

  completeness:
    score: 5
    reason: Clearly explains the motivation, philosophy, scope, use cases, non-goals, and success criteria of the project.

  complexity:
    score: 4
    reason: Covers multiple architectural concerns including abstraction layers, execution surfaces, plugin systems, and configuration management.

  importance:
    score: 5
    reason: Acts as the foundational vision document guiding the entire project.

  career_relevance:
    score: 5
    reason: Demonstrates software architecture, framework design, developer tooling, and platform engineering skills valuable for senior engineering roles.

  freshness:
    score: 5
    reason: Reflects modern internal developer platform patterns using FastAPI, Typer, Celery, webhooks, and declarative configuration.

  reusability:
    score: 5
    reason: Architectural principles can be reused across similar internal tooling and platform projects.

  review_priority:
    score: 4
    reason: Core design document that should evolve alongside architectural decisions and implementation.

  connectedness:
    score: 5
    reason: Will connect to ADRs, architecture diagrams, implementation notes, plugins, configuration schemas, and API documentation.

  actionability:
    score: 4
    reason: Defines concrete design constraints and success criteria, though implementation details live elsewhere.

  quality_score:
    score: 95
    reason: Concise, focused, and comprehensive vision document with clear boundaries, architectural principles, and measurable goals.

custom:
  subdomain: developer-platform

  tags:
    - cli2api
    - developer-platform
    - fastapi
    - typer
    - architecture

ai_summary: >
  Vision document for cli2api, a lightweight internal developer platform that exposes a single Python function as multiple execution surfaces including CLI commands, REST APIs, asynchronous jobs, and automation webhooks. The architecture separates business logic, declarative YAML configuration, and execution plugins to eliminate boilerplate while keeping functions framework-agnostic. The note defines the project's philosophy, target use cases, non-goals, and success criteria, serving as the architectural foundation for future implementation.
```

### Why I classified it this way

- **Domain → `software-engineering`** because the primary focus is framework/platform design rather than Python syntax or backend implementation.
    
- **Note Type → `architecture`** because this is essentially an architectural vision/README. It's not a project plan or tutorial—it explains _what the system is, why it exists, and its design principles_.
    
- **Status → `curated`** because it reads like a stable vision document that should change infrequently.
    
- **Folder → `Projects/cli2api`** because this is the root note (README) for the project and should become the hub linking ADRs, architecture diagrams, implementation notes, plugin design, YAML schema, and API generation.