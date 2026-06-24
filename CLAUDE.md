---
type: concept
---

# CLAUDE.md

Guidance for Claude Code (claude.ai/code) when working in this repo.

## Repository Type

**Obsidian personal knowledge vault** — not a code project. No build/lint/test pipeline. No `package.json`, `pyproject.toml`, source tree. Files = markdown notes (some HTML/JSX exports for Obsidian plugins). Commits = auto-generated vault backups (see git log).

## Structure (Top-Level)

| Folder | Purpose |
|---|---|
| `00 Interview Questions/` | Topic-organized interview prep (Data Eng, Cloud, Cost, etc.). Cross-links to `01 Curated/` and `02 Reference/`. |
| `00 Projects/` | One subfolder per project: `Healthcare/`, `LakeMind/`, `PowerShell/`, `Test Automation - CAI/`, `Xpose/`. |
| `00 Prompts/` | Reusable LLM prompt templates (summarizers, optimizers, job apps). |
| `01 Curated/` | Synthesis, decisions, trade-offs, project analyses — "what I think about X". Deep-dive concept notes, tool analyses, decision frameworks. |
| `02 Reference/` | Evergreen factual reference — syntax, definitions, how-to lookups. No narrative, no opinions. |
| `03 Career Vault/` | Career-long compounding knowledge: ADRs, open questions, lessons/trade-offs, incidents/postmortems. |
| `Python Libs Collection.md` | Flat list of ~640 Python tools/frameworks/tags. |
| `Storage Tracker.md` | Personal storage/inventory tracker. |
| `claude_response.md` | Output of prior reclassification task on `Python Libs Collection.md` — 33-domain grouped taxonomy. |
| `interview_prep.jsx`, `workspace-system-design.html` | Exported Obsidian workspace snapshots. |
| `.obsidian/` | Obsidian config (workspace, plugins, themes). Do not edit by hand. |

### Knowledge Philosophy

- **Curated** = synthesis + decisions. Notes with a voice. "Here's what I think about X and why."
- **Reference** = lookup. Factual, no narrative. "How do I do X syntax."
- **Career Vault** = compounding expertise. ADRs, lessons, open questions, incident analyses.
- **Interview Questions** = Q&A format prep. Each links back to Curated/Reference for deeper study.
- Knowledge is organized around *problems and projects*, not technologies.

## Conventions & Working Patterns

- **Naming**: Folders prefixed `00 ` = user-prioritized; numbered siblings sort first. Single-topic files = topic as title (`LakeHouse.md`). Multi-topic = `Topic — Subtopic.md` (em-dash, not hyphen).
- **Wikilinks**: Cross-references use `[[Topic]]` (Obsidian-native). Preserve when editing; converting to plain links breaks graph.
- **Git**: Commits = timestamped "vault backup: YYYY-MM-DD HH:MM:SS" auto-commits. Don't force re-bumps; let backup flow handle.
- **Deletions**: Several project folders removed in recent commits (AI-Driven Batch Optimization Platform, Query Plan Intelligence, etc.). Files move between top-level notes and project folders; check git log before assuming gone.

## Common Tasks in This Repo

- **Reclassify a list file** (e.g. `Python Libs Collection.md`) → write grouped output to `claude_response.md` or sibling. See `claude_response.md` for established 33-domain taxonomy to reuse/extend.
- **Add interview prep on a topic** → drop `Topic.md` into `00 Interview Questions/`. Match existing em-dash + Title Case style. If refactoring existing file, preserve `[[wikilinks]]` and answer patterns; verify all wikilinks resolve before committing.
- **Spin up a project** → create `00 Projects/<Project Name>/<Project Name>.md` with project description. See existing projects for shape.
- **Update Python Libs taxonomy** → edit `claude_response.md`; keep cross-reference appendix in sync.

## Do Not

- Don't run npm/pip/pytest/etc. — nothing to build.
- Don't edit anything under `.obsidian/` — plugin state.
- Don't strip `[[wikilinks]]` or `##tags` (Obsidian metadata).
- Don't assume tool/framework is "live code" — most are research references only.
