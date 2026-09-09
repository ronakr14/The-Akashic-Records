---
note_type: moc
status: log
created: 2026-09-09
---
# Daily Tech Briefings — Index

The dated notes here are AI-generated tech briefings, not personal capture. `00-Daily/` root is the capture layer; briefings live here as a running feed.

This index deduplicates ~130 story headings across 25 briefings (2026-08-13 → 2026-09-09) into recurring themes and links each to the knowledge it connects to, so the feed feeds the graph instead of sitting inert. Chronological list: [[_Briefing MOC]].

---

## Recurring themes

### Postgres / DuckDB as an agent primitive

Databricks (Lakebase as an app database for AI ×several, Postgres-in-sandbox, edge), DuckDB 2.0 client/server → alpha, AWS hiring the DuckDB team, ClickHouse local data engine for agents, Aurora MySQL multi-source replication, Kimi's disposable-compute + persistent-state, India's sovereign Postgres+AI layer.

- [[Database Design]] · [[Query Optimization]] · [[Polars]] · [[Parquet]] · [[Vector Database]] · [[DuckDB]] · [[Data Lake]]
- Experiment (repeated across briefings): benchmark Pandas → Polars → DuckDB on Parquet; DuckDB 2.0 alpha worth a real test

### MCP as infrastructure and governance

MongoDB Atlas managed MCP, AWS MCP governance, Nutanix control-plane MCP, Oracle controlled MCP workflow, Microsoft Fabric Real-Time MCP, Snowflake agentic control plane, Anthropic Model Hardware Standard ("MCP for machines").

- [[_AI Tools Catalog]] (Nanobot, Token Optimizer MCP) · [[_AI MOC]] · [[Database Design]]
- Experiment: constrained read-only MCP server over local Postgres — schema allowlist, query timeout, row limit, audit every call

### Agent identity, authorization, security

Google Cloud agent identity as infra primitive, AWS stateful (not just permission-based) authz + agent detection-and-response, Fortinet/Virtue AI, AID-Guard (approval ≠ action), TRACE (portable proof of what ran), agent security incident format, Snowflake gVisor Snowpark sandbox rebuild, rogue-agent incident (behaviour outside the system boundary), agentic vulnerability discovery (Google Mantis, Cloudflare vuln→prod-traffic), AI-generated infra code security gap, India agentic-UPI authorization.

- [[Password Storage]] · [[Distributed System]] · [[_AI Tools Catalog]] (SkillSpector, OBLITERATUS) · [[Defending Code Reference Harness]]

### The harness matters more than the model

NVIDIA AVO + Switchyard cost-based router, GitHub HydraFusion (model selection as a runtime systems problem), DeepSeek Harness open-sourcing the layer around the model, Anthropic multi-agent token burn, "hidden cost is orchestration not the model", Databricks AI SRE / "what a production agent looks like", parallel-agent workflows vs the single-agent loop, Tutti context handoff.

- [[Agent Architecture]] · [[_AI MOC]] · [[_AI Tools Catalog]] (HALO, Omnigent, GStack, Paseo)

### Lakehouse → real-time serving + federated context layer

Databricks real-time serving + automatic optimization + Automatic Change Data Feed + Genie Ontology, Cloudera Anywhere distributed control plane, Iceberg Variant for messy event data, AWS Glue 6.0 (Iceberg v3, Spark 4.1), AWS+Google cross-cloud Iceberg, Google federated context layer + Hive Metastore migration.

- [[Data Vault & Lakehouse Modelling]] · [[Lakehouse Performance Optimization]] · [[Delta Lake & Iceberg]] · [[Stream Processing]] · [[Incremental Data Loading Strategies]] · [[Data Mesh]]

### Inference as a distributed-systems discipline

Ray Summit + first vLLM Conference, the memory wall, LLM training efficiency levers, local AI as its own infra category, NVIDIA acquiring Hugging Face ($12.93B — open-model infra as strategic), Unsloth Desktop local-first fine-tuning, OpenAI Jalapeño hardware/software co-design, Cloudflare RAM/cache savings from "boring" systems engineering.

- [[LLM Serving & Inference]] · [[Distributed System]] · [[_AI Tools Catalog]] (CrowdLlama, Distributed Llama, Hugging Face Accelerate)

### RAG cost: compress, don't just retrieve less

- [[Vector Database]] · [[_AI MOC]] (RAG + context-engineering gaps)

### Production evaluation beats benchmarks

GitHub LLM eval work, SWE Refactor Bench weaknesses, OpenAI agent-first internal experiment, OpenAI Astra / GPT-6 forcing a "capability threshold" conversation.

- [[Model Evaluation]] · [[_AI MOC]]

### Agent cost / FinOps

Databricks: $1.2M/year of agent waste hiding in failed MCP calls; separate finding on agent waste; orchestration as the hidden cost; cost-based model routers.

- [[Model Evaluation]] · [[Agent Architecture]] · [[Data Engineering Playbook]] (observability principles)

### Graph as agent context

BigQuery Graph GA, Databricks Genie Ontology, Meta's "organizational second brain" — structured/graph context as the interface for agents rather than raw tables.

- [[Data Modelling]] · [[Vector Database]] · [[Context Engineering]] · [[Vault Vision]]

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

PrimeAgentOrchestrator's PKM-friendly memory approach; Meta's "organizational second brain" (close to this vault's architecture — knowledge graph + retrieval + synthesis).

- [[Vault Vision]] · [[Akashic Engine Build Checklist]] · [[PKM Knowledge Refresh System – Review & Enhancements]]

---

## Promotion candidates

Themes with enough repetition to synthesize. Each already has a draft note — drop the briefing specifics in when filling it:

- **Agent-ready data access** (MCP governance, "stop giving agents SQL", MongoDB/AWS/Oracle/Snowflake MCP) → [[Context Engineering]] (governed-context section) + [[Agent Architecture]] (tools/MCP section)
- **Agent harness > model** (NVIDIA AVO/Switchyard, DeepSeek harness, Anthropic multi-agent token burn) → [[Agent Architecture]] (harness-vs-model section)
- **Distributed inference / memory wall** (Ray + first vLLM Conference, LLM training efficiency, local AI as infra) → [[LLM Serving & Inference]]
- **Production eval beats benchmarks** (GitHub eval work, SWE Refactor Bench) → [[Model Evaluation]] (production-evaluation section)
- **RAG cost: compress, don't retrieve less** → [[Retrieval-Augmented Generation]] + [[Context Engineering]]

Writing angles for the same material: [[_Writing MOC]]

## Refresh

Re-fold new briefs into the themes above roughly every 10–15 briefs. Last refresh: 2026-09-09 (through brief 2026-09-09).

## See also

- [[_Briefing MOC]] — chronological list of all briefs
- [[_Data Engineering MOC]] · [[_AI MOC]] · [[_Writing MOC]]
