---
type: concept
---

# ADRs — Architecture Decision Records

> A decision with context. Not just *what* was chosen, but *why* and *at what cost*.

## Format

Each ADR includes:

```markdown
# [Title]

**Date:** YYYY-MM-DD
**Status:** Accepted / Deprecated / Superseded
**Deciders:** [Who made this decision]

## Context
What's the situation? What forces are at play (tech, business, team)?

## Decision
What did we decide?

## Consequences
- Positive: ...
- Negative: ...
- Risks: ...

## Alternatives Considered
- Option A: why rejected
- Option B: why rejected

## See Also
- [[related-note]]
```

## Entries

- [[Bloom Filters - Row Group Pruning]] — 2026-06-25 — adopt Bloom Filters for high-cardinality equality pruning in Parquet row groups
