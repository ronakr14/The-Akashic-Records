---
domain: prompt
subdomain: vault-maintenance
note_type: prompt
source_type: self
status: draft
level: intermediate
---
# AI Summary
Prompt for classifying and scoring a vault note. The categorical fields and their LOVs mirror `90-System/schema.md` exactly (single source of truth) — emit them as frontmatter in schema key order. The rating fields are inputs for the intelligence layer / manual review, not frontmatter. Also produces a title, folder, subdomain, and an AI Summary.

---

Classify the following note.

- **title**: suitable title based on content
- **folder**: suitable folder based on content

## Frontmatter fields

Choose exactly one value from each LOV — do not invent values. One-line reason for each. These LOVs are copied from `90-System/schema.md`; if that file changes, this list is wrong, not the schema.

1. **domain**: `data-engineering | software-engineering | ai | career | cloud | database | python | pkm | architecture | prompt | tool`
2. **subdomain**: free-form short slug, lowercase-with-hyphens, most specific fit (e.g. `spark-streaming`, `vector-database`, `system-design`). Reuse an existing slug where one fits.
3. **note_type**: `concept | technology | project | adr | tutorial | interview | architecture | glossary | snippet | template | prompt | moc`
4. **source_type**: `web | book | github | obsidian | paper | video | course | self`
5. **status**: `inbox | draft | reference | curated | evergreen`
6. **level**: `beginner | intermediate | advanced`

Emit as YAML frontmatter in this exact key order: `domain, subdomain, note_type, source_type, status, level`.

## AI Summary

A summary of the note's content, under 100 words, descriptive enough to locate the note from the summary alone. This is the first body section (`# AI Summary`), before a `---` and the content.

## Rating fields (intelligence-layer inputs, NOT frontmatter)

Score 1–5 with the given criteria. These feed the review queue / Akashic Engine; they are not written into the note.

- **Confidence** — how trustworthy: 1 Rough notes · 2 Needs verification · 3 Reliable sources · 4 Validated · 5 Frequently used
- **Completeness** — answers its own question (what/why/how, examples, pitfalls, refs): 1 Skeleton · 2 Major gaps · 3 Good overview · 4 Practical coverage · 5 Exhaustive
- **Complexity** — difficulty to understand: 1 Simple definition · 2 Small concept · 3 Multi-step · 4 System-level · 5 Deep architecture/research
- **Importance** — to your career: 1 Nice to know · 2 Occasional · 3 Useful · 4 Frequent · 5 Critical
- **Career relevance** — maps to target roles: 1 Hobby · 2 Peripheral · 3 Helpful · 4 Relevant · 5 Core/work
- **Freshness** — recency of validation: 1 Outdated · 2 Last year · 3 Within a year · 4 Within 6 months · 5 This month
- **Reusability** — across contexts: 1 One-off · 2 Limited · 3 Useful · 4 Reusable · 5 Universal
- **Review priority** — `importance × career_relevance × freshness_decay × (1/confidence)`: 1 Review in 1 year · 2 6 months · 3 3 months · 4 1 month · 5 2 weeks
- **Connectedness** — graph centrality (in+out links / vault size): 1 Orphan · 2 Few · 3 Moderate · 4 Many · 5 Hub
- **Actionability**: 1 Informational · 2 Conceptual · 3 Practical · 4 Instructional · 5 Executable
- **Quality score** — overall 0–100

The deterministic version of Connectedness / Freshness / a Quality score is computed by `.repo-metadata/health_report.py` — see [[Vault Dashboard]].
