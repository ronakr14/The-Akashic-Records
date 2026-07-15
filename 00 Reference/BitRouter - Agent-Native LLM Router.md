```table-of-contents
```


> **Source**: [github.com/bitrouter/bitrouter](https://github.com/bitrouter/bitrouter)
> **Current release**: v1.0.0-alpha.10
> **Language**: Rust (100%)

## What It Is

BitRouter is an open-source, Rust-based LLM routing and gateway platform designed for AI agents. It acts as a local proxy between AI applications/agents and multiple LLM providers (OpenAI, Anthropic, Google Gemini, Bedrock, OpenRouter, etc.).

Think of it as a **"Kubernetes Ingress Controller for LLMs"** — focused on model routing, failover, cost optimization, security guardrails, observability, and agent interoperability.

## Problem It Solves

Organizations building AI agents face:

- **Vendor lock-in** — tied to a single provider's API and pricing
- **API outages** — single point of failure when the provider goes down
- **Cost overruns** — no visibility or control over per-request spending
- **Security concerns** — no centralized policy enforcement for prompts/outputs
- **Model sprawl** — managing dozens of models across providers manually

BitRouter abstracts all providers behind a unified routing layer, solving these without modifying agent code.

## Architecture

```
                AI Agent
                    |
                    v
             +-------------+
             |  BitRouter  |
             +-------------+
              /    |     \
             /     |      \
            v      v       v
        OpenAI  Anthropic  Gemini
```

### Data Flow

```
Prompt → BitRouter → Policy Engine → Routing Engine → Guardrails → Provider Adapter → Provider
                                                                        Response returns through same chain
```

### Repository Structure

| Directory | Purpose |
|---|---|
| `apps/bitrouter` | Main executable: CLI, proxy startup, runtime management |
| `crates/` | Core framework: routing engine, provider adapters, policies, metrics |
| `mcp/` | Model Context Protocol server: tool orchestration, agent interoperability |
| `plugins/` | Provider extensions |
| `skills/` | Agent Skills framework for self-configuration and automation |

## Core Features

### Routing
- Model selection, provider selection, cost-aware routing, intent-aware routing

### Reliability
- Automatic failover, multi-provider fallback, load balancing

### Security
- Prompt injection detection, output filtering, secret redaction, virtual API keys

### Observability
- Cost tracking, request tracing, Prometheus metrics, OTLP export

### Agent Support
- Claude Code, Codex, OpenCode, OpenClaw, Hermes, MCP, ACP

### Protocol Translation
- OpenAI → Anthropic, OpenAI → Gemini, cross-provider interoperability

## Unique Differentiators

- **Agent-native design** — most gateways are human-centric; BitRouter targets autonomous agents
- **Cross-protocol routing** — translate requests across provider APIs transparently
- **MCP + ACP integration** — few routers support both protocols
- **Local-first architecture** — runs locally, no forced SaaS adoption

## Comparison with Alternatives

| Feature | BitRouter | LiteLLM | OpenRouter |
|---|---|---|---|
| Open Source | Yes | Yes | No |
| Self-Hosted | Yes | Yes | No |
| Agent-Focused | Yes | Partial | No |
| Rust | Yes | No | N/A |
| MCP Support | Yes | Limited | No |
| Guardrails | Built-in | Add-ons | Hosted |
| Cost Tracking | Strong | Medium | Medium |

Closest competitor is **LiteLLM**. BitRouter is potentially superior for agent infrastructure due to MCP/ACP support and Rust performance.

## Installation & Deployment

```bash
# Homebrew
brew install bitrouter/tap/bitrouter

# NPM
npm install -g bitrouter

# Cargo
cargo install bitrouter
```

**Deployment targets**: local dev machine, container, VM, Kubernetes.

**Infrastructure requirements**: minimal (1+ CPU, 512MB–2GB RAM, small storage). Most load is upstream to LLMs.

## Evaluation

### Strengths
- Strong architecture with Rust workspace structure
- Plugin-oriented extensibility
- Single environment variable change for adoption
- Observability and routing capabilities are unusually strong for a young project

### Weaknesses
- Alpha release — not yet enterprise-proven at scale
- Small community (~176 stars)
- No large-scale production references yet
- Potential API instability due to rapid evolution

### Scores

| Category | Score |
|---|---|
| Production Readiness | 7/10 |
| Security | 8/10 |
| Scalability | 8/10 |
| Observability | 9/10 |
| Documentation | 7/10 |
| Community | 5/10 |
| Maintainability | 8/10 |

### Recommendation

| Scenario | Verdict |
|---|---|
| Startup AI Platform | Use |
| Internal AI Gateway | Use |
| Agent Platform | Use |
| Enterprise Pilot | Evaluate |
| Large Regulated Enterprise | Evaluate |
| Mission-Critical Production | Evaluate Carefully |

Best fit: AI platform teams, agent infrastructure, internal AI gateways, multi-provider environments. Avoid for now: mission-critical regulated workloads requiring proven enterprise support.

## Relevance to Data & AI Engineering

**Data platforms**: metadata assistants, data catalogs, data quality agents, query optimization copilots, semantic layers.

**Lakehouse integration**: BitRouter becomes the AI control plane sitting between agents and the lakehouse (Databricks, Iceberg, DuckDB, Trino, Spark).

**ETL/ELT** (indirect): SQL generation, pipeline debugging, root cause analysis, data quality recommendations.

**LLM/RAG/Agents** (strongest use case):
- RAG: retrieval agent routing, embedding model routing, cost optimization
- Agents: multi-agent orchestration, tool invocation governance, failover management
- LLM Platforms: unified model access, central governance

### Enterprise Architecture Pattern

```
Users → AI Applications → BitRouter (Routing / Guardrails / Cost Control / Observability)
                                |
                    OpenAI  Anthropic  Gemini
                                |
                          Agent Layer
                                |
                    RAG / MCP / Workflows
                                |
              Lakehouse (Iceberg + Spark + Trino + DuckDB)
```

## Engineering Takeaways

**Good patterns**: Gateway pattern (centralized control plane), Adapter pattern (provider abstraction), Policy Enforcement Layer (security before execution), Sidecar deployment, Local-first design.

**Architectural lessons**: Separate routing from application logic, centralize observability, centralize guardrails, decouple providers.

**Anti-patterns to watch**: Too many routing policies become difficult to reason about; cross-provider behavior may introduce subtle compatibility issues.

## Related

- [[LLM Routing]]
- [[MCP]]
- [[Prompt Injection]]
- [[LiteLLM]]
- [[OpenRouter]]
- [[AI Gateway]]
- [[Cost Optimization]]
