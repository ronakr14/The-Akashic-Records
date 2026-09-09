---
domain: ai
subdomain: context-engineering
note_type: concept
source_type: self
status: draft
level: advanced
---
# AI Summary

DRAFT — scaffold only. Synthesis pending. Managing what goes into the context window: budgeting, retrieval, compaction, and governed context — the briefings' recurring "data engineer becomes context engineer" thesis, and the vault's own [[Vault Vision]] concern.

---

## The window as a budget

- Token accounting: system + tools + history + retrieved + output headroom
- Cost and latency scale with context; lost-in-the-middle

## What earns a place in context

- Task-relevant only; ranking and dropping
- Static (instructions, schema) vs dynamic (retrieved, tool output)

## Compaction

- Rolling summary, hierarchical summary, structured state notes
- When to compact vs when to retrieve fresh — see [[Retrieval-Augmented Generation]]

## Governed / semantic context

- Metadata, catalogs, semantic layer as the interface for agents (briefings theme)
- "Stop giving agents raw SQL" — constrain before generation
- Connects to [[Data Mesh]], [[Data Vault & Lakehouse Modelling]]

## Context for agents

- Per-step context assembly, scratchpad hygiene
- See [[Agent Architecture]] memory section

## Prompt vs context

- When the fix is context selection, not prompt wording — see [[Prompt Engineering]]

## Open questions

- Retrieval budget vs summary budget split for long agent runs?
- How to measure context quality directly (not just end-task score)?

## Reference

- [[Token Optimizer MCP]] — context/token reduction
- [[_Briefings Index]] — "data engineer → context engineer" theme
- [[_Writing MOC]] — the article backlog around this topic
- [[_AI Tools Catalog]]

## See also

- [[_AI MOC]] · [[Retrieval-Augmented Generation]] · [[Agent Architecture]] · [[Prompt Engineering]] · [[Vault Vision]]
