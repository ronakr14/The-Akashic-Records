---
domain: architecture
subdomain: execution-platform
note_type: moc
source_type: self
status: curated
level: advanced
---
# AI Summary

Project hub for cli2api — a framework that exposes one Python function as CLI, REST API, and async-worker surfaces from a single registry. Indexes the design, roadmap, and integration notes, and points at the `01-Knowledge/` notes the project depends on.

---

# cli2api — Project Map

## Vision & principles

- [[Design Goals]] — what cli2api is, target use cases, non-goals, success criteria
- [[Design Principles]] — architectural constraints, anti-patterns, production trade-offs
- [[cli2api System Architecture]] — registry, binding layer, execution pipeline, Redis infra

## Build plan

- [[Implementation Roadmap]] — seven incremental phases, MVP → platform
- [[Feature Roadmap and Enhancements]] — planned feature set beyond core
- [[Plugin System]] — lifecycle hooks, ordering, discovery, built-in plugin catalog
- [[Examples and Reference Implementations]] — hands-on, simple function → production deploy

## Integrations

- [[Integration - Typer]] — CLI generation (preferred)
- [[Integration - Argparse]] — discouraged; when it still applies
- [[Integration - Rich]] — terminal output formatting

## Prerequisite knowledge

- [[FastAPI Authentication]] · [[Microservices]] · [[Distributed System]]
- [[Idempotency in Data Pipelines]] · [[Python - Modules & Packages]] · [[Python External Libraries Playbook]]

## See also

- [[_Architecture MOC]] · [[_Software Engineering MOC]]
