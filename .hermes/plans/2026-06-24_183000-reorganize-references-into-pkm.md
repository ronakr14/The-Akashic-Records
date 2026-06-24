---
type: concept
---

# PKM Vault Reorganization — References → Curated + Reference + Projects

> **Goal:** Restructure the vault so knowledge is organized around *problems and projects* rather than technologies. Separate permanent reference (evergreen principles) from curated/synthesis notes (decisions, trade-offs, project analyses). Move tool-specific quick-reference out of the main knowledge graph.

**Architecture:** Three top-level pillars — `01 Curated/` (synthesis, decisions, career lessons, ADRs, open questions), `02 Reference/` (evergreen permanent reference), `00 Projects/` (project-specific work). A new `03 Career Vault/` captures lessons/trade-offs/incidents. Interview questions stay under `00 Interview Questions/` but gain wikilinks into the curated/reference pillars.

**Current state:**
- `00 References/` — 43 files, mixed bag: evergreen reference (Distributed System, Idempotency), project/curated analysis (OpenSpec, BitRouter, Anthropic harness), tool quick-reference (VSCode Debug, Git Multi Account, Compare File in Powershell), and Python syntax notes.
- `00 Interview Questions/` — 15 files, some overlap with Reference topics (Partitioning, LakeHouse, Microservices).
- `00 Projects/` — 5 project folders (Healthcare, LakeMind, PowerShell, Test Automation - CAI, Xpose).
- No `01 Curated/` or `03 Career Vault/` exists yet.

---

## Step-by-Step Plan

### Phase 1: Create new top-level structure

**Task 1: Create folders**

Create:
- `01 Curated/`
- `02 Reference/`
- `03 Career Vault/` (with subfolders: `ADRs/`, `Open Questions/`, `Lessons & Trade-offs/`, `Incidents & Postmortems/`)

No files yet — just directories.

---

### Phase 2: Move curated/synthesis notes → `01 Curated/`

**Criteria for "Curated":** Notes that synthesize multiple sources, document decisions/trade-offs, analyze a tool/project, or capture "what I think about X." These are *written by me, for my future self* — they have a point of view.

**Files to move from `00 References/` → `01 Curated/`:**

| File | Why curated |
|---|---|
| `Data Engineering Playbook.md` | Synthesized 15 core truths — synthesis, not raw reference |
| `LLM Interaction Guide.md` | Opinionated framework (exploration vs decision mode) |
| `OpenSpec.md` | Project analysis report with executive summary |
| `BitRouter - Agent-Native LLM Router.md` | Project analysis (architecture, problem mapping) |
| `Anthropic - Defending Code Reference Harness.md` | Deep analysis report, 1200 lines |
| `RyanCodrai - Turbovec.md` | Vendor/tool analysis |
| `Password Storage.md` | Decision guide (Argon2id preferred, with reasoning) |
| `Idempotency.md` | Concept note with delivery semantics — connects theory to practice |
| `Distributed System.md` | 1600-line deep dive — this is *curated learning*, not quick reference |
| `python.md` | 189-line Python overview — curated synthesis of Python fundamentals |
| `Python External Libraries Playbook.md` | Curated library recommendations |
| `Python Environment Playbook.md` | Opinionated workflow guide (uv recommended) |
| `Stream Data Processing.md` | 1038-line concept deep-dive |
| `Delta Lake's OPTIMIZE.md` | 676-line "most misunderstood" synthesis |
| `Data Modelling.md` | Concept + checklist synthesis |
| `Data Modelling Checklist.md` | Decision tool |
| `Data Vault & Lakehouse Modelling.md` | Comparative synthesis |
| `Data Mesh.md` | Concept synthesis |
| `Data Lake.md` | Concept synthesis |
| `Bloom Filters.md` | Concept deep-dive |
| `Vector Database.md` | Concept deep-dive |
| `UUIDv7 & ULID.md` | Concept + comparison |
| `Z-Ordering.md` | Concept deep-dive |
| `Monolithic System.md` | Concept synthesis |
| `Microservice.md` | Concept synthesis |
| `ETL vs ELT.md` | Decision framework |
| `Incremental Load Strategy.md` | Strategy pattern |
| `Batch Processing.md` | Concept synthesis |
| `Partitioning.md` | Concept + strategy |
| `Parquet.md` | Format deep-dive |

**Rationale:** These all have a *voice* — they explain, compare, recommend, or synthesize. They're not "look up the syntax" notes. They belong in the curated layer where I can find "what do I think about X" quickly.

---

### Phase 3: Move permanent reference → `02 Reference/`

**Criteria for "Reference":** Evergreen, factual, no opinion — "look up the syntax/behavior." Short-lived utility. Quick lookup.

**Files to move from `00 References/` → `02 Reference/`:**

| File | Why reference |
|---|---|
| `python — OOP & Classes.md` | Syntax reference |
| `python — Concurrency.md` | Syntax reference |
| `python — Modules & Packages.md` | Syntax reference |
| `python — Files & Serialization.md` | Syntax reference |
| `ETL.md` | Definition/reference |
| `ELT.md` | Definition/reference |
| `DuckDB.md` | Tool reference |
| `Delta Lake & Iceberg.md` | Technology comparison (factual) |
| `Git Multi Account Setup.md` | How-to quick reference |
| `VSCode Debug.md` | How-to quick reference |
| `Compare File in Powershell.md` | How-to quick reference |
| `OpenSpec.md` | *(moved to Curated in Phase 2 — remove from this list)* |

**Wait — correction:** `OpenSpec.md` stays in Curated. Final `02 Reference/` list:

`python — OOP & Classes.md`, `python — Concurrency.md`, `python — Modules & Packages.md`, `python — Files & Serialization.md`, `ETL.md`, `ELT.md`, `DuckDB.md`, `Delta Lake & Iceberg.md`, `Git Multi Account Setup.md`, `VSCode Debug.md`, `Compare File in Powershell.md`

**Rationale:** These are "I need to remember how to do X" notes. They have no narrative. They belong in a separate layer so they don't clutter the curated synthesis space.

---

### Phase 4: Move tool/environment notes → `00 Projects/` or absorb

**Observation:** Some reference notes are so tool-specific they might belong in a project context rather than the knowledge vault at all.

**Files to evaluate:**

| File | Destination | Reason |
|---|---|---|
| `Python Environment Playbook.md` | Keep in `01 Curated/` (already moved) | Opinionated workflow — curated |
| `Git Multi Account Setup.md` | `02 Reference/` | Quick how-to |
| `VSCode Debug.md` | `02 Reference/` | Quick how-to |
| `Compare File in Powershell.md` | `00 Projects/PowerShell/` | PowerShell project-specific |
| `PowerShell Profile.md` | Already in `00 Projects/PowerShell/` | Already in place |

**Action:** Move `Compare File in Powershell.md` → `00 Projects/PowerShell/`

---

### Phase 5: Build `03 Career Vault/`

**Task 5: Create structure + seed from existing content**

Create folders:
- `03 Career Vault/ADRs/` — Architecture Decision Records
- `03 Career Vault/Open Questions/` — Unresolved questions
- `03 Career Vault/Lessons & Trade-offs/` — Experience-derived lessons
- `03 Career Vault/Incidents & Postmortems/` — Failure analyses

**Seed files (create new, empty scaffolding):**
- `03 Career Vault/README.md` — Purpose + folder guide + how to add entries
- `03 Career Vault/ADRs/YYYY-MM-DD-template.md` — ADR template
- `03 Career Vault/Open Questions/README.md` — Index of open questions
- `03 Career Vault/Lessons & Trade-offs/README.md` — Index
- `03 Career Vault/Incidents & Postmortems/README.md` — Index

**No existing files move here** — this is a new space. Future notes from project postmortems, real ADRs, and lessons learned will populate it.

---

### Phase 6: Deduplicate Interview Questions vs Curated/Reference

**Observation:** Several interview Q&A files duplicate content already in Curated/Reference:

| Interview file | Overlaps with (Curated/Reference) | Action |
|---|---|---|
| `Partitioning.md` | `01 Curated/Partitioning.md` (after move) | Keep interview version — it has expected-answer format. Add `→ See also: [[Partitioning]]` link |
| `LakeHouse.md` | `01 Curated/Data Lake.md`, `01 Curated/Delta Lake & Iceberg.md` | Keep interview version. Add wikilinks to curated notes |
| `Microservices.md` | `01 Curated/Microservice.md`, `01 Curated/Monolithic System.md` | Keep interview version. Add wikilinks |
| `ETL vs ELT Interview.md` | `01 Curated/ETL vs ELT.md` | Keep interview version. Add wikilink |
| `Batch Processing - Modern.md` | `01 Curated/Batch Processing.md` | Keep interview version. Add wikilink |
| `Batch Processing - Advance.md` | `01 Curated/Batch Processing.md` | Keep interview version. Add wikilink |
| `Incremental Processing.md` | `01 Curated/Incremental Load Strategy.md` | Keep interview version. Add wikilink |
| `Failure Recovery.md` | `01 Curated/Idempotency.md` | Keep interview version. Add wikilink |
| `Metadata & Observability.md` | No direct match | Keep — unique content |
| `Data Quality.md` | No direct match | Keep — unique content |
| `Performance Optimization.md` | No direct match | Keep — unique content |
| `Query Optimization.md` | No direct match | Keep — unique content |
| `System Design.md` | `01 Curated/Distributed System.md` | Keep interview version. Add wikilink |
| `Fundamentals.md` | Overlaps with multiple | Keep interview version. Add wikilinks |
| `Senior Python Data Engineer — Interview Prep.md` | Python reference files | Keep interview version. Add wikilinks |

**Action:** No interview files are deleted. Each gets a "See also" wikilink section at the bottom pointing to the corresponding curated/reference notes. This creates the graph between interview prep and knowledge.

---

### Phase 7: Update CLAUDE.md and cross-references

**Task 7: Update CLAUDE.md**

Update the "Structure (Top-Level)" table and "Conventions" section to reflect the new folder layout:

```
| `01 Curated/` | Synthesis, decisions, trade-offs, project analyses — "what I think about X" |
| `02 Reference/` | Evergreen factual reference — syntax, definitions, how-to lookups |
| `03 Career Vault/` | ADRs, open questions, lessons, incidents — career-long compounding knowledge |
```

Update the "Common Tasks" section to reference the new PKM philosophy.

**Task 8: Add wikilinks between Curated ↔ Reference**

For each curated note that has a corresponding reference note, add a "See Also" section:
```markdown
## See Also
- [[Idempotency]] (reference) ← from curated distributed systems note
- [[Partitioning]] (curated) ← from reference note if needed
```

---

### Phase 8: Clean up `00 References/`

After all moves, `00 References/` should be empty. Delete the folder.

---

## Final Folder Structure

```
The-Akashic-Records/
├── 00 Interview Questions/     (15 files — interview prep, wikilinked to curated/ref)
├── 00 Projects/                (5 project folders — project-specific work)
├── 00 Prompts/                 (prompt templates — unchanged)
├── 01 Curated/                 (~28 files — synthesis, decisions, analyses)
│   ├── Data Engineering Playbook.md
│   ├── Distributed System.md
│   ├── Idempotency.md
│   ├── LLM Interaction Guide.md
│   ├── OpenSpec.md
│   ├── BitRouter - Agent-Native LLM Router.md
│   ├── Anthropic - Defending Code Reference Harness.md
│   ├── Password Storage.md
│   ├── Stream Data Processing.md
│   ├── Delta Lake's OPTIMIZE.md
│   ├── Data Modelling.md
│   ├── Data Modelling Checklist.md
│   ├── Data Vault & Lakehouse Modelling.md
│   ├── Data Mesh.md
│   ├── Data Lake.md
│   ├── Bloom Filters.md
│   ├── Vector Database.md
│   ├── UUIDv7 & ULID.md
│   ├── Z-Ordering.md
│   ├── Monolithic System.md
│   ├── Microservice.md
│   ├── ETL vs ELT.md
│   ├── Incremental Load Strategy.md
│   ├── Batch Processing.md
│   ├── Partitioning.md
│   ├── Parquet.md
│   ├── python.md
│   ├── Python External Libraries Playbook.md
│   ├── Python Environment Playbook.md
│   ├── RyanCodrai - Turbovec.md
│   └── ... (etc)
├── 02 Reference/                (~11 files — quick lookup)
│   ├── python — OOP & Classes.md
│   ├── python — Concurrency.md
│   ├── python — Modules & Packages.md
│   ├── python — Files & Serialization.md
│   ├── ETL.md
│   ├── ELT.md
│   ├── DuckDB.md
│   ├── Delta Lake & Iceberg.md
│   ├── Git Multi Account Setup.md
│   ├── VSCode Debug.md
│   └── ... (etc)
├── 03 Career Vault/            (new — career compounding)
│   ├── ADRs/
│   ├── Open Questions/
│   ├── Lessons & Trade-offs/
│   └── Incidents & Postmortems/
├── Catalog.md                  (unchanged)
├── CLAUDE.md                   (updated)
├── Python Libs Collection.md   (unchanged)
├── Storage Tracker.md          (unchanged)
└── workspace-system-design.html (unchanged)
```

---

## Risks & Trade-offs

1. **Broken wikilinks during move** — Obsidian `[[Title]]` links break if the file moves to a different *title* (folder change doesn't break them, but renaming does). Plan: move files without renaming. Verify with Obsidian graph after.
2. **Interview ↔ Curated duplication** — Some content is very similar. Solution: keep both, cross-link. The interview version has Q&A format; the curated version has synthesis format. They serve different retrieval scenarios.
3. **"Curated" vs "Reference" boundary is fuzzy** — Some files could go either way (e.g., `Delta Lake & Iceberg.md`). Default rule: if it has opinions/recommendations → Curated; if it's factual lookup → Reference.
4. **Career Vault is empty at first** — This is intentional. It's a structure to capture future learnings, not a migration target.

---

## Verification

After execution:
1. `ls 00 References/` → should not exist (or empty)
2. `ls 01 Curated/ | wc -l` → ~28 files
3. `ls 02 Reference/ | wc -l` → ~11 files
4. `ls 03 Career Vault/` → 4 subfolders with README files
5. Open Obsidian → graph view shows connections between Curated ↔ Interview ↔ Projects
6. Spot-check 5 random wikilinks → all resolve
