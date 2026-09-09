---
domain: data-engineering
subdomain: healthcare-lakehouse
note_type: moc
source_type: self
status: curated
level: advanced
---
# AI Summary

Project hub for the Intelligent Healthcare Data & AI Platform — an 11-phase build from an operational healthcare backend through a Bronze/Silver/Gold lakehouse to ML, RAG, and agent workloads. Indexes the domain, phase, and roadmap notes, and maps each stage to its prerequisite `01-Knowledge/` notes.

---

# Healthcare Data & AI Platform — Project Map

## Roadmaps

- [[Intelligent Healthcare Data & AI Platform Roadmap]] — full 11-phase blueprint (primary)
- [[Roadmap]] — analytics / ML / RAG / agent capability roadmap

## Domain model

- [[Healthcare Domain Model]] — core business domains, entities, RBAC, encounters
- [[Healthcare Domain Events]] — patient-lifecycle event catalog (event-driven foundation)
- [[Patient Workflow]] — end-to-end operational workflows
- [[Resource Lifecycle]] — bed / ventilator / medicine state machines

## Phase 1 — backend foundation

- [[Phase 1 - Core Healthcare Platform (Backend Foundation)]] — scope, deliverables
- [[Phase 1 MVP - Core Healthcare Platform Implementation Plan]] — narrowed 2-week MVP plan

## Prerequisite knowledge

- Backend: [[FastAPI Authentication]] · [[Password Storage]] · [[Microservices]] · [[Monolithic System]] · [[Database Design]] · [[UUIDv7 & ULID]]
- Pipelines: [[Batch Processing]] · [[Stream Processing]] · [[Incremental Data Loading Strategies]] · [[Idempotency in Data Pipelines]] · [[Failure Recovery in Batch Data Pipelines]]
- Lakehouse: [[Data Vault & Lakehouse Modelling]] · [[Data Modelling]] · [[Lakehouse Performance Optimization]] · [[Partitioning]] · [[Z-Ordering]] · [[Parquet]] · [[PySpark]] · [[Query Optimization]]
- AI: [[Vector Database]] · [[LLM Interaction Guide]] · [[_AI MOC]]

## See also

- [[_Data Engineering MOC]] · [[_Architecture MOC]] · [[_Software Engineering MOC]]
