---
note_type: moc
status: log
created: 2026-09-09
---
# Daily Tech Briefings — Index

The dated notes here are AI-generated tech briefings, not personal capture. `00-Daily/` root is the capture layer; briefings live here as a running feed.

This index deduplicates ~85 story headings across the briefings into recurring themes and links each to the knowledge it connects to, so the feed feeds the graph instead of sitting inert.

---

## Recurring themes

### Postgres / DuckDB as an agent primitive

Databricks (Lakebase, Postgres-in-sandbox, edge), DuckDB 2.0 client/server, AWS hiring the DuckDB team, Kimi's disposable-compute + persistent-state, India's sovereign Postgres+AI layer.

- [[Database Design]] · [[Query Optimization]] · [[Polars]] · [[Parquet]] · [[Vector Database]]
- Experiment (repeated across briefings): benchmark Pandas → Polars → DuckDB on Parquet

### MCP as infrastructure and governance

MongoDB Atlas managed MCP, AWS MCP governance, Nutanix control-plane MCP, Oracle controlled MCP workflow, Microsoft Fabric Real-Time MCP, Snowflake agentic control plane, Anthropic Model Hardware Standard ("MCP for machines").

- [[_AI Tools Catalog]] (Nanobot, Token Optimizer MCP) · [[_AI MOC]] · [[Database Design]]
- Experiment: constrained read-only MCP server over local Postgres — schema allowlist, query timeout, row limit, audit every call

### Agent identity, authorization, security

Google Cloud agent identity as infra primitive, AWS stateful (not just permission-based) authz, Fortinet/Virtue AI, AID-Guard (approval ≠ action), TRACE (portable proof of what ran), agent security incident format.

- [[Password Storage]] · [[Distributed System]] · [[_AI Tools Catalog]] (SkillSpector, OBLITERATUS)

### The harness matters more than the model

NVIDIA AVO + Switchyard cost-based router, DeepSeek open-sourcing the layer around the model, Anthropic multi-agent token burn, "hidden cost is orchestration not the model".

- [[_AI MOC]] (agent-architecture gap) · [[_AI Tools Catalog]] (HALO, Omnigent, GStack, Paseo)

### Lakehouse → real-time serving + federated context layer

Databricks real-time serving, Cloudera Anywhere distributed control plane, Iceberg Variant for messy event data, Google federated context layer + Hive Metastore migration.

- [[Data Vault & Lakehouse Modelling]] · [[Lakehouse Performance Optimization]] · [[Stream Processing]] · [[Data Mesh]]

### Inference as a distributed-systems discipline

Ray Summit + first vLLM Conference, the memory wall, LLM training efficiency levers, local AI as its own infra category.

- [[Distributed System]] · [[_AI MOC]] (LLM-serving gap) · [[_AI Tools Catalog]] (CrowdLlama, Distributed Llama, Hugging Face Accelerate)

### RAG cost: compress, don't just retrieve less

- [[Vector Database]] · [[_AI MOC]] (RAG + context-engineering gaps)

### Production evaluation beats benchmarks

GitHub LLM eval work, SWE Refactor Bench weaknesses, OpenAI agent-first internal experiment.

- [[_AI MOC]] (model-evaluation gap)

### Agentic data engineering keeps AI out of the production runtime

AWS reference architecture, real-time Dataflow with adaptive execution.

- [[Batch Processing]] · [[Idempotency in Data Pipelines]] · [[Failure Recovery in Batch Data Pipelines]]

### Repo / IDE as agent control plane

GitHub agent control plane + Agentic Workflows, Cursor Origin, Warp software factory, Zide, Positron.

- [[_cli2api MOC]] (function → surface platform pattern) · [[Distributed System]]

### AI career signal

McKinsey 2026 survey reality check, job market rewarding "AI + infrastructure + architecture", senior ladder disruption, forward-deployed engineering, Debian/Linux AI-contribution votes.

- [[_Interview MOC]] · [[End-to-End Learning Goals for AI Data Platform Project]]

### PKM-relevant: agent long-term memory

PrimeAgentOrchestrator's PKM-friendly memory approach.

- [[Vault Vision]] · [[Akashic Engine Build Checklist]] · [[PKM Knowledge Refresh System – Review & Enhancements]]

---

## Promotion candidates

Themes above with enough repetition to justify a synthesized note:

- **Agent-ready data access** (MCP governance + "stop giving agents SQL") → new note under `01-Knowledge/ai/` or `architecture/`; fills [[_AI MOC]] context-engineering gap
- **Agent harness architecture** → fills [[_AI MOC]] agent-architecture gap
- **Distributed inference** → fills [[_AI MOC]] LLM-serving gap

Writing angles for the same material: [[_Writing MOC]]

## See also

- [[_Data Engineering MOC]] · [[_AI MOC]] · [[_Writing MOC]]
