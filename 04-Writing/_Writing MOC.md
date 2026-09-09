---
domain: pkm
subdomain: writing
note_type: moc
source_type: self
status: draft
level: intermediate
---
# AI Summary

Hub for technical-writing output. The dated notes in `Ideas/` are raw weekly topic dumps (AI-generated); this MOC deduplicates them into one backlog and maps each candidate article to the `01-Knowledge/` notes and projects that already back it — so writing draws on accumulated knowledge instead of starting cold.

---

# Writing — Map of Content

## Idea backlog (consolidated)

Recurring candidates across the weekly dumps, most-repeated first. "Backed by" = material already in the vault.

### 1. Data Engineer → Context Engineer

Appears in every weekly dump. Thesis: the role is shifting from pipelines to governed context (metadata, semantics, catalogs, MCP).

- Backed by: [[_Data Engineering MOC]] · [[_AI MOC]] · [[Vector Database]] · [[Data Mesh]] · [[Data Modelling]]
- Project example: [[Intelligent Healthcare Data & AI Platform Roadmap]]
- Fills AI MOC gap: "Context engineering"

### 2. MCP for Data Engineers

The 2026-07-28 stateless-core spec as a concrete anchor; architecture angle over tutorial.

- Backed by: [[_AI Tools Catalog]] (Nanobot, Token Optimizer MCP) · [[_AI MOC]] · [[FastAPI Authentication]] · [[Database Design]]

### 3. Building an AI-native PKM

Engineering decisions behind this vault, not another Obsidian setup guide.

- Backed by: [[Vault Vision]] · [[PKM Knowledge Refresh System – Review & Enhancements]] · [[Akashic Engine Build Checklist]] · [[Obsidian Learning Map]]

### 4. Reverse-engineering DuckDB

Columnar / vectorized execution deep-dive; recurring "Reverse Engineering" series seed.

- Backed by: [[Query Optimization]] · [[Parquet]] · [[Polars]] · [[_AI Tools Catalog]] (repo-analysis format)

### 5. Semantic layer for AI agents

Why governed metrics/definitions must sit between agents and raw tables.

- Backed by: [[Data Vault & Lakehouse Modelling]] · [[Data Mesh]] · [[Data Modelling]] · [[_AI MOC]]

### 6. Framework-agnostic AI agents

Clean architecture, tool abstraction, plugin lifecycle, no framework lock-in.

- Backed by: [[_cli2api MOC]] · [[Design Principles]] · [[Plugin System]] · [[_AI Tools Catalog]]

### 7. AI-ready lakehouses

What changes in lakehouse architecture for agent workloads vs BI.

- Backed by: [[Data Vault & Lakehouse Modelling]] · [[Lakehouse Performance Optimization]] · [[Partitioning]] · [[Z-Ordering]] · [[Intelligent Healthcare Data & AI Platform Roadmap]]

### 8. From ETL pipelines to agentic data workflows

Pipeline as one component inside a discover → plan → execute → validate → observe → retry loop.

- Backed by: [[Batch Processing]] · [[Failure Recovery in Batch Data Pipelines]] · [[Idempotency in Data Pipelines]] · [[_AI MOC]]

### Opinion pieces

- **"Your AI agent should not have SQL access"** — [[Database Design]] · [[Password Storage]] · [[Data Mesh]]
- **"AI won't replace data engineers, bad data will"** — [[Data Engineering Playbook]] · [[Data Quality in Batch Pipelines]] · [[Metadata & Observability]]

## Source dumps

- [[20260731]] · [[20260807]] · [[20260814]] · [[20260821]]

## Pipeline

`Ideas/` → Drafts → Published. No Drafts or Published notes yet.
