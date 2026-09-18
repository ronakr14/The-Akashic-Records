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

Appears in nearly every weekly dump. Thesis: the role is shifting from pipelines to governed context (metadata, semantics, catalogs, MCP).

- Backed by: [[_Data Engineering MOC]] · [[_AI MOC]] · [[Vector Database]] · [[Data Mesh]] · [[Data Modelling]] · [[Context Engineering]]
- Project example: [[Intelligent Healthcare Data & AI Platform Roadmap]]
- Fills AI MOC gap: "Context engineering"

### 2. DuckDB 2.0: the embedded database becomes a data service

The #1 pick in the last three dumps (09-04, 09-11, 09-18). DuckDB 2.0 alpha + the Quack extension turn DuckDB into a client/server system (remote instances, concurrent access, compute near data); AWS hiring the DuckDB team raises the open-source-stewardship question. Also the seed for a recurring "Reverse Engineering" series (columnar / vectorized execution deep-dive).

- Backed by: [[DuckDB]] · [[Query Optimization]] · [[Parquet]] · [[Polars]] · [[_AI Tools Catalog]] (repo-analysis format)
- Experiment: embedded vs Quack client/server on the same Parquet workload — latency, concurrency, where each breaks

### 3. Agent identity & the MCP security boundary

Merges four angles: MCP gateways as the new data-platform security boundary (09-04), MCP security as its own discipline (09-11), "the MCP spec ≠ a security boundary" (09-18), and agent identity/authorization in the MCP era — the 09-18 "what I'd write" pick. Arc: data → context → tools → agents → identity → authorization → governance.

- Backed by: [[Password Storage]] · [[FastAPI Authentication]] · [[Agent Architecture]] · [[Defending Code Reference Harness]] · [[_Briefings Index]] (agent identity/security theme)
- Demo: three-hop delegated agent workflow with an audit trail — who initiated → which agent delegated → what authority → which MCP tool → what data/action

### 4. MCP for Data Engineers

The 2026-07-28 stateless-core spec as a concrete anchor; architecture angle over tutorial.

- Backed by: [[_AI Tools Catalog]] (Nanobot, Token Optimizer MCP) · [[_AI MOC]] · [[FastAPI Authentication]] · [[Database Design]]

### 5. Agent Skills vs RAG vs MCP — where should AI get its context?

The 09-11 "what I'd write" pick. One task, four context strategies, same model and tools — measure the difference. Seed for a reusable context-engineering benchmark.

- Backed by: [[Context Engineering]] · [[Retrieval-Augmented Generation]] · [[Model Evaluation]] · [[Prompt Engineering]]

### 6. Semantic layer / governance as AI context

Why governed metrics/definitions must sit between agents and raw tables. Folds in "governance artifacts are becoming AI context" (09-11) and "AI agents need a data contract too" (09-04).

- Backed by: [[Data Vault & Lakehouse Modelling]] · [[Data Mesh]] · [[Data Modelling]] · [[Metadata & Observability]] · [[_AI MOC]]

### 7. Building an AI-native PKM

Engineering decisions behind this vault, not another Obsidian setup guide.

- Backed by: [[Vault Vision]] · [[PKM Knowledge Refresh System – Review & Enhancements]] · [[Akashic Engine Build Checklist]] · [[Obsidian Learning Map]]

### 8. Framework-agnostic AI agents

Clean architecture, tool abstraction, plugin lifecycle, no framework lock-in.

- Backed by: [[_cli2api MOC]] · [[Design Principles]] · [[Plugin System]] · [[_AI Tools Catalog]]

### 9. AI-ready lakehouses

What changes in lakehouse architecture for agent workloads vs BI. Includes the VARIANT thread: DuckDB + VARIANT (09-04) and Iceberg Variant for storing agent data (09-18).

- Backed by: [[Data Vault & Lakehouse Modelling]] · [[Lakehouse Performance Optimization]] · [[Delta Lake & Iceberg]] · [[Partitioning]] · [[Z-Ordering]] · [[Intelligent Healthcare Data & AI Platform Roadmap]]

### 10. From ETL pipelines to agentic data workflows

Pipeline as one component inside a discover → plan → execute → validate → observe → retry loop. 09-18 framing: agent → plan → execute → verify.

- Backed by: [[Batch Processing]] · [[Failure Recovery in Batch Data Pipelines]] · [[Idempotency in Data Pipelines]] · [[_AI MOC]]

### 11. RAG is a data-engineering problem

Chunking, embedding refresh, and index maintenance as incremental pipelines with the usual correctness problems (09-11).

- Backed by: [[Retrieval-Augmented Generation]] · [[Vector Database]] · [[Incremental Data Loading Strategies]] · [[Idempotency in Data Pipelines]]

### 12. AI inference is becoming a data-engineering workload

Batch inference, scheduling, and cost as pipeline concerns (09-11).

- Backed by: [[LLM Serving & Inference]] · [[Batch Processing]] · [[Distributed LLM]] (home-lab measurements could supply real numbers)

### Opinion pieces

- **"Your AI agent should not have SQL access / a database password"** (repeated 09-18) — [[Database Design]] · [[Password Storage]] · [[Data Mesh]] · [[Neon]] (MCP branching as the safer alternative)
- **"AI won't replace data engineers, bad data will"** — [[Data Engineering Playbook]] · [[Data Quality in Batch Pipelines]] · [[Metadata & Observability]]

## Source dumps

Path-qualified — bare `YYYY-MM-DD` names also exist under `00-Daily/Briefings/`.

- [[04-Writing/Ideas/2026-07-31|2026-07-31]]
- [[04-Writing/Ideas/2026-08-07|2026-08-07]]
- [[04-Writing/Ideas/2026-08-14|2026-08-14]]
- [[04-Writing/Ideas/2026-08-21|2026-08-21]]
- [[04-Writing/Ideas/2026-08-28|2026-08-28]]
- [[04-Writing/Ideas/2026-09-04|2026-09-04]]
- [[04-Writing/Ideas/2026-09-11|2026-09-11]]
- [[04-Writing/Ideas/2026-09-18|2026-09-18]]

Last folded: 2026-09-18 (through dump 2026-09-18).

## Pipeline

`Ideas/` → Drafts → Published. No Drafts or Published notes yet.
