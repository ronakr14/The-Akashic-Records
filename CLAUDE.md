# CLAUDE.md

Guidance for Claude Code (claude.ai/code) when working in this repo.

## Repository Type

**Obsidian personal knowledge vault** — not a code project. No build/lint/test pipeline. No `package.json`, `pyproject.toml`, source tree. Files = markdown notes (some HTML/JSX exports for Obsidian plugins). Commits = auto-generated vault backups (see git log).

## Structure (Top-Level)

| Folder | Purpose |
|---|---|
| `00 Interview Questions/` | Topic-organized interview prep (Data Eng, Cloud, Cost, etc.) |
| `00 Projects/` | One subfolder per project: `FastAPI CLI Decorator/`, `Lakehouse Optimizer/`, `Test Automation - CAI/`, `GitHub Sync/`, `Healthcare/`. Some prior projects deleted in recent commits. |
| `00 Prompts/` | Reusable LLM prompt templates (summarizers, optimizers, job apps). |
| `00 References/` | Long-form reference notes (Data Engineering Playbook, Distributed System, GIT, etc.). |
| `Artificial Intelligence/`, `Cloud Computing/`, `Data Engineering/` | Domain notes. |
| `Python Libs Collection.md` | Flat list of ~640 Python tools/frameworks/tags. |
| `Storage Tracker.md` | Personal storage/inventory tracker. |
| `claude_response.md` | Output of prior reclassification task on `Python Libs Collection.md` — 33-domain grouped taxonomy. |
| `interview_prep.jsx`, `workspace-system-design.html` | Exported Obsidian workspace snapshots. |
| `.obsidian/` | Obsidian config (workspace, plugins, themes). Do not edit by hand. |

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
