---
domain: ai
subdomain: agents
note_type: concept
source_type: self
status: draft
level: advanced
---
# AI Summary

DRAFT — scaffold only. Synthesis pending. How an LLM agent is put together: the control loop, tool interface, memory, planning, and the multi-agent question — plus why the harness around the model often matters more than the model.

---

## The core loop

- Perceive → plan → act (tool call) → observe → repeat → stop
- Stopping criteria, step budgets, loop detection

## Tools

- Tool schema design, argument validation, error surfaces
- MCP as a standard tool interface — see [[_Briefings Index]] (MCP-as-infrastructure theme)
- Read-only vs mutating tools, approval gates

## Memory

- Working context vs episodic vs long-term store
- Summarisation / compaction — connects to [[Context Engineering]]
- Retrieval over past runs — connects to [[Retrieval-Augmented Generation]]

## Planning

- ReAct, plan-then-execute, tree/graph search, reflection
- When explicit planning beats a plain loop

## Multi-agent

- Orchestrator + workers, hand-off, shared scratchpad
- Token cost of multi-agent (briefings: Anthropic finding)
- When a single agent with better tools wins

## Harness vs model

- Verification, retries, sandboxing, deterministic scaffolding
- Briefings theme: NVIDIA AVO, DeepSeek harness — the loop carries the quality

## Failure modes

- Context rot over long runs, tool thrash, silent wrong-tool, unrecoverable state

## Open questions

- Where to put the planning/verification boundary?
- Durable agent state across restarts — how much, where?
- Evaluating an agent vs evaluating its model — see [[Model Evaluation]]

## Reference

- [[Nanobot]] · [[OpenHarness]] · [[AgentHatch]] · [[GStack]] — agent frameworks / runtimes
- [[Omnigent]] · [[Paseo]] — orchestration
- [[HALO (Hierarchal Agent Loop Optimizer)]] — loop optimisation / observability
- [[GBrain]] · [[OpenChronicle]] — agent memory
- [[ATLAS]] — agentic decision systems
- [[MiroThinker]] — research agents
- [[_AI Tools Catalog]]

## See also

- [[_AI MOC]] · [[Context Engineering]] · [[Retrieval-Augmented Generation]] · [[Model Evaluation]] · [[_cli2api MOC]]
