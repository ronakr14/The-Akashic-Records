# Frontmatter Schema

Single source of truth for note metadata in this vault. Every content note carries the same key set with values from the lists below. Journals and personal trackers use a reduced stub.

Rule: **metadata exists because the system uses it, not because it might be useful someday.**

---

## Standard schema (Knowledge, Projects, Prompts, Inbox)

```yaml
---
domain: <one of DOMAIN>
subdomain: <free-form slug, lowercase-with-hyphens, most specific fit>
note_type: <one of NOTE_TYPE>
source_type: <one of SOURCE_TYPE>
status: <one of STATUS>
level: <one of LEVEL>
---
```

Key order is fixed as above.

### DOMAIN

`data-engineering` | `software-engineering` | `ai` | `career` | `cloud` | `database` | `python` | `pkm` | `architecture` | `prompt` | `tool`

### NOTE_TYPE

`concept` | `technology` | `project` | `adr` | `tutorial` | `interview` | `architecture` | `glossary` | `snippet` | `template` | `prompt` | `moc`

- `concept` — an idea/pattern explained (CDC, idempotency, data mesh)
- `technology` — a specific tool/product/library (DuckDB, Polars, Istio)
- `project` — something being built; project docs, roadmaps, plans
- `adr` — a decision record: what was chosen and why
- `tutorial` — step-by-step how-to
- `interview` — interview prep / question banks
- `architecture` — architecture / design docs, principles, system breakdowns
- `glossary` — catalog / index / reference list spanning many topics
- `snippet` — a small reusable code or config fragment
- `template` — a reusable document skeleton
- `prompt` — a reusable LLM prompt or prompt pack
- `moc` — map of content: a hub note that indexes and links the notes of one domain

### SOURCE_TYPE

`web` | `book` | `github` | `obsidian` | `paper` | `video` | `course` | `self`

`self` = written from own knowledge/experience. `github` = derived from a repo. `web` = article/blog/docs.

### STATUS  (maturity lifecycle)

`inbox` → `draft` → `reference` | `curated` → `evergreen`

- `inbox` — captured, not yet triaged
- `draft` — being actively developed, not trustworthy yet
- `reference` — stable lookup material that will not be synthesized further (external docs, tech spec notes)
- `curated` — reviewed, linked, trustworthy
- `evergreen` — fully synthesized in own words, well connected, maintained

### LEVEL

`beginner` | `intermediate` | `advanced`

---

## Stub schema

### Daily notes (`00-Daily/`)

```yaml
---
note_type: daily
status: log
created: YYYY-MM-DD
---
```

### Writing ideas (`04-Writing/Ideas/`)

```yaml
---
note_type: idea
status: draft
created: YYYY-MM-DD
---
```

### Personal (`99 Personal/`)

```yaml
---
note_type: personal
status: log
---
```

---

## Notes

- `tags:` was removed vault-wide (2026-09-08) along with all `[[wikilinks]]`, to rebuild connections deliberately. Reintroduce tags later only as a controlled vocabulary, if a use emerges.
- `subdomain` is intentionally free-form. Keep it a lowercase hyphenated slug; reuse existing values where they fit rather than inventing near-duplicates.
- Body convention: first section is `# AI Summary` (<100 words), then `---`, then content.
