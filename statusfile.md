---
type: status
project: The-Akashic-Records
generated: 2026-07-22
audience: future-AI-models
---

# Repository Status — `The-Akashic-Records`

> **Read this first.** This file is the canonical entry point for any AI model
> touching this repo. It documents what the repository *is*, what lives inside
> it, how it is organized, what conventions are in force, and what the current
> state of the work is as of the generation date above. Update it whenever the
> shape or focus of the vault changes in a material way.

---

## 1. One-paragraph orientation

`The-Akashic-Records` is a **personal Obsidian vault used as a long-running
learning and reference library** for a senior data / platform engineer
("Ronak", the repo's git user). It is **not a software project**: there is no
application code, no `package.json`, no `pyproject.toml`, no CI, no test
suite. The repo is a single-user PKM (Personal Knowledge Management) surface
backed by an Obsidian installation, version-controlled with `git` via the
`obsidian-git` community plugin, and auto-backed-up on a regular cadence. The
**primary artifact is Markdown notes**, plus a few Univer/Excel-like sheets
embedded in Markdown and one HTML rendering of a workspace design.

## 2. Repository at a glance

| Attribute | Value |
|---|---|
| Type | Personal Obsidian vault (single-user PKM) |
| Path | `C:\Workspace\The-Akashic-Records` |
| Default branch | `master` (origin: `origin/master`) |
| Git history | 30+ commits, dominated by `vault backup: YYYY-MM-DD HH:MM:SS` auto-snapshots from `obsidian-git` |
| Latest commit | `9b5ba86 vault backup: 2026-07-22 21:45:48` |
| `.gitignore` | Only `Attachments/` is ignored — attachments stay local; notes are tracked |
| Markdown count | **~185 .md at root + 165 in `00 Reference` + 5 in `01 Career Vault` ≈ 350+ notes** |
| Wikilink density | **436 `[[…]]` inter-note links** across the corpus |
| Frontmatter usage | Minimal; `type:` is the only widely-used field; tags are **not** used at scale |
| Tag system | **None observed** — discovery relies on wikilinks, folder location, and full-text search |
| Code blocks | Heavy use of fenced code for architecture diagrams, Python, SQL, JSON, YAML |
| Diagrams | One `workspace-system-design.html` (≈57 KB, likely a Mermaid/excalidraw export) |
| Embedded data | `Storage Tracker.md` contains a Univer (Excel-like) sheet JSON; `daily-note`-style notes may carry similar embeds |
| Theme | `Obsidianite` (community theme) |
| No active development surface | No `src/`, no `tests/`, no `Makefile`, no Dockerfile, no lockfiles, no CI config |

## 3. Top-level directory layout

```
C:\Workspace\The-Akashic-Records
├── 00 Reference/                    # The library — 165 .md notes covering tools, concepts, and reference material
├── 01 Career Vault/                 # Personal long-term knowledge — scaffolded, currently mostly empty
│   ├── ADRs/
│   ├── Incidents & Postmortems/
│   ├── Lessons & Trade-offs/
│   └── Open Questions/
├── .claude/                         # Claude Code local config (settings.local.json — see §9)
├── .hermes/                         # Hermes-related scratch (only `plans/` subdir, currently empty)
├── .obsidian/                       # Obsidian app config + plugins + theme
├── *.md                             # ~15 large root-level deep-analysis reports (see §5)
├── Storage Tracker.md               # Embedded Univer sheet for personal cloud-storage accounting
├── workspace-system-design.html     # Static HTML export of a workspace design diagram
└── Untitled 2.md                    # Small scratch note (≈3.7 KB)
```

### 3.1 `00 Reference/` — the library

A **flat, name-as-slug** folder of reference notes. **No subfolders.** All
files sit at one level. Naming is `Title Case.md`, sometimes with em-dashes
(`—`) or version suffixes (`DuckDB.md` + `DuckDB 1.md`, `00 Goal.md` + `00
Goal (2).md`). This is the **largest and most actively used** area of the
vault.

Coverage spans five rough clusters, overlapping heavily:

1. **Data & platform engineering fundamentals** — ETL, ELT, Data Lake, Data
   Lakehouse, Data Warehouse, Data Mesh, Data Vault, Data Modelling, Delta
   Lake, Iceberg, Parquet, Snowflake, ClickHouse, DuckDB, DuckLake, Dask,
   Spark/PySpark, Kafka, RDD/Dataframe APIs, Partitioning, Optimization,
   Incremental Load, Idempotency, Bloom Filters, Distributed Systems,
   Database Design, Data Quality, Failure Recovery.
2. **Backend engineering** — FastAPI Auth, Idempotency, Modular vs Monolith
   Architecture, Microservices, Typer, Argparse, Rich, Python (Concurrency,
   Files & Serialization, Modules & Packages, OOP & Classes, External
   Libraries Playbook, Environment Playbook).
3. **ML / LLM / RAG / Agentic** — Embeddings, Vector DB, RAG, Evaluation,
   Feature Engineering, Model Training, Model Serving, Experiment Tracking,
   Langchain, LlamaIndex, PgVector, FAISS, MLOps, LLMOps, AgentOps, Tool
   Calling, Multi-Agent workflows, Memory, Planning.
4. **Specific OSS products and tools** — one or more notes per tool
   (e.g. `MongoDB.md`, `Neon.md`, `Archon.md`, `Obscura.md`, `OBLITERATUS.md`,
   `Onyx.md`, `Supertonic.md`, `AutoHedge.md`, `Database Skills.md`,
   `HomeButler.md`, `OpenChronicle.md`, `Atlas OS.md`, `Bloom Filters.md`,
   `CrowdLlama.md`, `Distributed Llama.md`, `GStack.md`, `PAUL.md`, `Omnigent.md`,
   `Lakekeeper.md`, `GBrain.md`, `OpenSandbox.md`, `Omniroute.md`, `CloakBrowser.md`,
   `Tuta.md`, `Repowise.md`, `Himalaya.md`, `Dockpeek.md`, `Token Optimizer MCP.md`,
   `Honcho.md`, `Gortex.md`, `Euria.md`, `Just.md`, `Erlang.md`, `Istio.md`,
   `Gitea.md`, `Cryptee.md`, `MailCore.md`, `Mailfence.md`, `MEGA.md`,
   `Nextcloud.md`, `LibreOffice.md`, `Hugging Face Accelerate.md`, `Koalas.md`,
   `The Fuzz.md`, `User Dialogs.md`, `Knowledge Catalog.md`, `Catalog.md`,
   `BitRouter - Agent-Native LLM Router.md`, `Claude Code Router.md`,
   `Anthropic - Defending Code Reference Harness.md`, `Defending Code Reference
   Harness.md`, `AgentHatch.md`, `AgentRQ.md`, `Agentic Resource Discovery.md`,
   `Test Automation - CAI.md`, `OpenHarness.md`, `Go AgentX.md`, `9Router.md`,
   `Dask.md`, `Spark.md`, etc).
5. **Career / workflow meta** — `Cover Letter.md`, `Resume — Optimization.md`,
   `LinkedIn — Profile Audit.md`, `Profile — README Rewrite.md`,
   `Interview — Prep.md`, `ATS — Hard Mode.md`, `Business Doc.md`,
   `Business Questions.md`, `Senior Python Data Engineer — Interview Prep.md`,
   `End of Session — Handoff.md`, `Daily Note — Update.md`,
   `Feedback — Extract.md`, `PKM Knowledge Refresh System – Review &
   Enhancements.md`, `Repo — Deep Analysis.md`.

### 3.2 `01 Career Vault/` — long-term personal knowledge

PARA-style "Projects" subfolder repurposed as a *career-long* knowledge
surface. README states the purpose:

> *"Career-long compounding knowledge. Not project-specific — how I think
> about engineering."*

Four subfolders with explicit naming and trigger conventions:

| Subfolder | Purpose | File-naming convention |
|---|---|---|
| `ADRs/` | Architectural decision records (why, not what) | `YYYY-MM-DD-<slug>.md` |
| `Open Questions/` | Unresolved but tracked questions | `Q-<slug>.md` |
| `Lessons & Trade-offs/` | "If I could go back, I'd…" | `LESSON-<slug>.md` |
| `Incidents & Postmortems/` | Failure analyses | `INC-<YYYY-MM-DD>-<slug>.md` |

**Current state: all four subfolders are empty save for a `README.md` each.**
The only entry that exists anywhere is referenced as a wikilink from
`ADRs/README.md`: `[[Bloom Filters — Row Group Pruning]]` — 2026-06-25, an
ADR about adopting Bloom Filters for high-cardinality equality pruning in
Parquet row groups. Treat the Career Vault as **scaffolded, not yet
populated**; do not assume an entry exists unless a wikilink confirms it.

### 3.3 Root-level `.md` files

~15 large (≈25–45 KB each) deep-analysis reports on individual OSS
repositories. They follow a common AI-generated structure (Executive Summary
→ Repository Overview → How It Works → Why It Exists → How It Can Be Used →
etc.) and cite the upstream GitHub repos. They are **not the user's own
projects** — they are research artifacts, likely produced by an external LLM
(consistent style with ChatGPT-style "Here is a deep-dive…" framing) and
saved into the vault as reference material.

| File | Upstream project |
|---|---|
| `Archon.md` | `coleam00/Archon` (AI-coding workflow engine) |
| `Atlas OS.md` | `Atlas-OS/Atlas` (Windows debloat / mod OS) |
| `AutoHedge.md` | `The-Swarm-Corporation/AutoHedge` |
| `Database Skills.md` | `planetscale/database-skills` |
| `HomeButler.md` | `Higangssh/homebutler` |
| `MongoDB.md` | `mongodb/mongo` (server codebase) |
| `Neon.md` | `neondatabase/neon` (serverless Postgres) |
| `OBLITERATUS.md` | `elder-plinius/OBLITERATUS` (mechanistic-interpretability LLM jailbreak research) |
| `Obscura.md` | `h4ckf0r0day/obscura` |
| `Onyx.md` | `onyx-dot-app/onyx` |
| `OpenChronicle.md` | `Einsia/OpenChronicle` |
| `Supertonic.md` | `supertone-inc/supertonic` (on-device multilingual TTS) |

> **Implication for AI agents:** these are *reading material*, not project
> code. Treat them as authoritative summaries of those upstream projects at
> the time they were written. If asked to update or verify their content,
> re-fetch from the cited GitHub URLs and diff against the current state.

### 3.4 Other root files

- `Storage Tracker.md` — Personal cloud-storage accounting sheet. Embedded
  Univer/Excel JSON block. Lists accounts (multiple `@gmail.com` /
  `@outlook.com` / `@zoho.in` addresses and one phone-tied Jio Cloud),
  providers (Google Drive, OneDrive, Mega, Jio Cloud), capacities (5/15/20
  GB typical), and notes (e.g. "Health & Custom", "Obsidian Library",
  "Marriage Photos & Other", "Books", "DPCOE"). Not a tool target — **personal
  data, do not edit without explicit user consent.**
- `workspace-system-design.html` — Static HTML export of a workspace design
  diagram (≈57 KB). Treat as an artifact snapshot; no live tool to update it.
- `Untitled 2.md` — Small (~3.7 KB) scratch note.
- `README.md` — 3 lines, only declares repo name. **Not a useful entry point.**

## 4. Obsidian configuration

### 4.1 Core plugins (`.obsidian/core-plugins.json`)

Enabled: file-explorer, global-search, switcher, graph, backlink, canvas,
outgoing-link, tag-pane, properties, page-preview, daily-notes, slash-command,
editor-status, markdown-importer, random-note, outline, audio-recorder.

Notably **disabled**: templates, command-palette, bookmarks, word-count,
slides, workspaces, file-recovery, publish, sync, bases, webviewer, footnotes,
zk-prefixer, note-composer.

### 4.2 Community plugins (`.obsidian/community-plugins.json`)

| Plugin | Use |
|---|---|
| `table-editor-obsidian` | Visual table editing |
| `automatic-table-of-contents` | Auto-TOC in headers |
| `editing-toolbar` | WYSIWYG-style toolbar |
| `iconic` | Per-icon customization (Holo, v1.1.9) |
| `sheet-plus` | Univer/Excel-like sheets in notes (powers `Storage Tracker.md`) |
| `obsidian-tomorrows-daily-note` | Daily-note shortcut |
| `obsidian-git` | Auto git backup — source of the `vault backup: …` commit stream |

### 4.3 App / appearance

- `app.json`: properties visible in-document, line numbers on, `openBehavior:
  daily`, new-file location = root, attachment folder = `Attachments/`,
  always-update-links, markdown-style links.
- `appearance.json`: theme = `Obsidianite` (single community theme installed).

## 5. Conventions and style

Inferred from the corpus — **these are observations, not enforced rules**:

- **No tag system.** Do not introduce tags silently; the user organizes by
  folder location, wikilinks, and full-text search.
- **Title Case filenames** with em-dashes (`—`) used for separators and
  version suffixes (` (2)`, ` 1`).
- **Wikilinks are the primary connection mechanism.** When creating or
  updating a note, prefer `[[Existing Note]]` over markdown links when the
  target is in the same vault.
- **Frontmatter is rare and minimal.** When present it uses YAML with `type:`
  as the dominant field (`concept`, `project`, `adr`, `question` observed).
  `excel-pro-plugin: parsed` appears on the storage-tracker note. Do not
  invent frontmatter conventions that the corpus doesn't already use.
- **Code blocks are widely used** for architecture diagrams (` ```text`),
  Python, SQL, JSON, YAML, shell. Preserve code-block formatting on edits.
- **One-line quote/lede per note** is common (line under the title).
- **No templates directory** exists, despite a `Daily Note — Update.md`
  reference. The `templates` core plugin is disabled.
- **No `Daily/` folder** exists at the root — daily notes are not separated
  into a dedicated folder. They may live at the root (per `newFileLocation:
  root`).

## 6. Git and backup state

- **Branches:** `master` (local + origin). No feature branches. No tags.
- **Commit shape:** ~all commits are `vault backup: YYYY-MM-DD HH:MM:SS` from
  `obsidian-git`. A few historical `temp` commits exist at the bottom of the
  log.
- **Commit cadence:** Daily to every-few-days; most recent gap is one day
  (2026-07-21 → 2026-07-22). The vault is actively maintained.
- **Working tree at generation time:** Clean except `M .obsidian/workspace.json`
  (an Obsidian-generated file). This is normal and should not be committed by
  hand; `obsidian-git` will pick it up on the next auto-backup.
- **No `.gitattributes`**, no LFS, no submodules.
- **No `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `Makefile`
  / Dockerfile / CI config.** Nothing to build, nothing to test, nothing to
  deploy.

## 7. Currently active work and themes (read from note content)

The vault's content reveals a **clear, sustained learning agenda**. A future
AI model can orient itself to the user's intent from these themes:

1. **Data-platform engineering depth** — ETL/ELT, lakehouse (Delta/Iceberg),
   Spark, Kafka, distributed systems, Parquet, Bloom Filters, idempotency,
   incremental load, data quality, data modelling, dbt-style patterns.
2. **ML / LLM / RAG / agentic AI literacy** — RAG evaluation, embeddings,
   vector DBs, agent orchestration, MLOps/LLMOps/AgentOps.
3. **OSS landscape scouting** — many deep-dive reports on third-party
   projects (Archon, MongoDB server, Neon, Onyx, Atlas-OS, OBLITERATUS,
   Supertonic, etc.). The user is **mapping the ecosystem**, not building
   these projects.
4. **Career craft** — Resume optimization, LinkedIn audit, README rewrite,
   interview prep (notably "Senior Python Data Engineer"), ATS-hard-mode,
   cover letter. The `01 Career Vault` is being seeded toward long-term
   compounding.
5. **A capstone project being spec'd in-repo** — `00 Reference/00 Proposal.md`
   lays out an **"Intelligent Healthcare Data & AI Platform"** with 11
   phases (Backend → Batch → Distributed → Streaming → Warehouse → ML → MLOps
   → RAG → Agentic → Multi-Agent → LLMOps/AgentOps). A trimmed Phase 1
   ("Trimmed Scope") is documented separately. **This is a spec / roadmap,
   not started code.** Subsequent notes `00 Goal (2).md`, `00 Goal.md`, and
   `01 Goal.md` describe the *learning* goals behind that capstone.
6. **A DataTest Automation project spec** —
   `00 Reference/2026-06-19_120000-datatest-automation.md` describes an
   "LLM-driven data test automation framework on Databricks" called
   "DataTest Forge". Three-phase pipeline (Excel → Markdown → Test Assets →
   Execution), SQLite as control plane, Python inside Databricks notebooks,
   HITL gates per phase. **Spec only, not started code.**
7. **PKM-vault self-improvement** — `00 Reference/PKM Knowledge Refresh
   System – Review & Enhancements.md` and `00 Reference/Repo — Deep
   Analysis.md` are meta-notes about *this vault itself*: knowledge-graph
   generation, daily review, agent workspace (Career Architect, Data
   Engineering Mentor, PKM Curator, Project Reviewer, Interview Coach),
   knowledge quality scoring (completeness, freshness, reusability,
   connectedness, confidence, review-priority).
8. **Caveman-mode tooling is in active use.** The `Caveman.md` reference
   describes the JuliusBrussee/caveman skill toolkit (output compression
   modes `lite|full|ultra`, slash commands, multi-agent install). The local
   `.claude/settings.local.json` is the Claude Code allowlist for safe shell
   commands. The user is **already operating in caveman mode** as observed
   in this session.

## 8. Known data and non-code artifacts

| Artifact | Location | Notes |
|---|---|---|
| Storage accounting sheet | `Storage Tracker.md` | Embedded Univer JSON. Personal data — do not edit. |
| Workspace design render | `workspace-system-design.html` | Static HTML; snapshot in time. |
| Sheet JSON | `.obsidian/plugins/sheet-plus/data.json` | Local sheet-plus plugin state. |
| Theme | `.obsidian/themes/Obsidianite/` | Community theme. |
| `1.md` file | root | Actually named `2.md` (typo'd as `Untitled 2.md` is the other small one). 3.7 KB scratch. |
| `Untitled 2.md` | root | 3.7 KB scratch. |

## 9. Local-tooling config (`.claude/settings.local.json`)

A small Claude Code permissions allowlist. Permits only narrow `Bash` commands
matching these patterns (all read-only vault inspection):

```
awk -F/ '{print $1"/"$2}'
grep -c "\.md$"
grep "\.md$"
awk -F/ 'NF>1 {print $1"/"$2}'
awk -F/ '{print $2}'
sed 's/.*\.//'
awk '{print $5, $NF}'
find . -maxdepth 2 -type d -not -path "*/\.*"
awk -F: '{print $1}'
```

These exist to reduce permission prompts during routine vault surveying. They
do **not** authorize file mutations.

## 10. Working-tree state as of 2026-07-22

```
M .obsidian/workspace.json          # Obsidian's per-session workspace layout
```

No other files modified. The repo is otherwise clean and matches the most
recent `vault backup` snapshot.

## 11. Guidance for future AI models

1. **Treat this repo as a personal knowledge vault, not a codebase.** There
   is nothing to compile, test, or deploy. Most asks will be knowledge
   operations: writing, refactoring, summarizing, finding, linking notes.
2. **Preserve user voice and convention.** The user writes in mixed English;
   technical terms appear exact. Do not add tags, frontmatter, or templates
   the corpus does not already use. Do not rename files casually — the
   wikilink graph would break.
3. **Respect the wikilink graph.** When creating new notes, prefer
   `[[Existing Note]]` over markdown links. When a note is referenced
   multiple times, follow the convention of the existing entry.
4. **Do not edit personal data files** (`Storage Tracker.md`, anything under
   `01 Career Vault/` with personal content) without explicit confirmation.
5. **Use parallel investigation when surveying.** Reading 350+ files is
   impractical; prefer `Grep` / `Glob` plus targeted `Read`s of a handful of
   representative notes (e.g. `README.md`, `01 Career Vault/README.md`,
   `00 Reference/00 Proposal.md`, `00 Reference/00 Goal.md`).
6. **Cite upstream sources when restating product claims.** Most of the
   root-level `.md` files are summaries of upstream GitHub projects; their
   content will drift as those projects evolve. When in doubt, re-fetch and
   diff.
7. **The user is operating in caveman mode** by default. Match the tone:
   terse, fragment-OK, technical content exact, no filler. Switch to plain
   prose when (a) explaining irreversible actions, (b) describing a
   multi-step sequence where order matters, (c) the user asks to clarify or
   repeats themselves.
8. **Auto-backups run on a daily-ish cadence** via `obsidian-git`. Long
   sessions that produce many edits will be auto-committed as
   `vault backup: …` entries; you do not need to commit manually unless
   the user asks.
9. **`.hermes/plans/` is empty.** If a Hermes task plan appears, it will be
   new; do not assume prior plans exist.
10. **The 01 Career Vault is scaffolded but not populated.** Only one ADR is
    referenced (`[[Bloom Filters — Row Group Pruning]]` — 2026-06-25). Treat
    other entries as "not yet written" rather than "missing from summary."

## 12. What this statusfile is *not*

- It is **not** a software project's README, build manifest, or test plan.
- It is **not** a generated index of every note — use `Glob` / `Grep` for
  that.
- It is **not** a commit log or changelog — see `git log` for that.
- It is **not** auto-regenerated on every commit — it is hand-curated. Update
  it when the *shape* of the vault changes in a material way: new top-level
  folder, new convention, new tool, new active project, change of intent.

## 13. Quick-references for common asks

| Ask | Where to look |
|---|---|
| "What data-engineering topics have I covered?" | `00 Reference/` filenames (DuckDB, Delta Lake, Kafka, Parquet, Bloom Filters, Idempotency, …) |
| "What's my capstone plan?" | `00 Reference/00 Proposal.md` (11 phases) and `00 Reference/1.1 Trimmed Scope.md` (Phase 1 trimmed) |
| "What are my learning goals?" | `00 Reference/00 Goal.md` (DE / Backend / ML / LLM / Agentic / Ops checklist) and `00 Reference/00 Goal (2).md` (KG + recommendations + agents + scoring) |
| "What third-party projects have I studied?" | Root-level `*.md` (Archon, Atlas OS, MongoDB, Neon, Onyx, OBLITERATUS, Supertonic, OpenChronicle, AutoHedge, HomeButler, Database Skills, Obscura) plus `00 Reference/` (Caveman, CrowdLlama, Distributed Llama, GStack, PAUL, Omnigent, Lakekeeper, GBrain, OpenSandbox, Omniroute, …) |
| "Where do ADRs / lessons / postmortems go?" | `01 Career Vault/{ADRs,Lessons & Trade-offs,Incidents & Postmortems,Open Questions}/` — all currently empty except READMEs |
| "Where's my personal storage tracking?" | `Storage Tracker.md` (embedded Univer sheet; do not edit) |
| "What plugins does the vault use?" | `.obsidian/community-plugins.json` (7 enabled) and `.obsidian/core-plugins.json` |
| "How is the vault auto-backed-up?" | `obsidian-git` plugin, daily-ish, commits are `vault backup: …` |
| "What's the theme / look?" | `Obsidianite` (`.obsidian/themes/Obsidianite/`) |
| "Is there anything to build / test / deploy?" | No. This is a knowledge vault, not a codebase. |

## 14. Generation metadata

- **Generated:** 2026-07-22
- **Generator:** Claude (Caveman mode, full intensity) on behalf of the repo
  owner
- **Inputs at generation time:**
  - Full directory listing (depth 2)
  - `git ls-files`, `git log --oneline -30`, `git branch -a`
  - `Read` of `README.md`, `.gitignore`, `.obsidian/app.json`,
    `.obsidian/core-plugins.json`, `.obsidian/community-plugins.json`,
    `.obsidian/appearance.json`, `.claude/settings.local.json`,
    `01 Career Vault/README.md`, `01 Career Vault/ADRs/README.md`,
    `00 Reference/00 Goal.md`, `00 Reference/00 Goal (2).md`,
    `00 Reference/00 Proposal.md`, `00 Reference/02 Architecture.md`,
    `Storage Tracker.md` (truncated), `Archon.md` (first 80 lines)
  - `Grep` for wikilinks (top 20), frontmatter fields, `type:` values
  - File-size scan of all `.md` for top-30 by size
- **Subagents attempted:** 3 (sample vault, map tree, audit docs) — all
  429-rate-limited at generation time; data was collected via direct tool
  calls instead.
- **Limitations:** No code present means no static analysis. Notes have not
  been opened individually past the anchors listed above; the description
  of `00 Reference/` is based on filenames plus a sampling of high-signal
  notes (`00 Goal.md`, `00 Proposal.md`, `02 Architecture.md`, `1.1
  Trimmed Scope.md`, `Bloom Filters.md`, `Caveman.md`,
  `datatest-automation.md`).
