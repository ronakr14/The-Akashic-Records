# AI Summary
None. Done. I've written the full phasewise checklist with explicit passing criteria to:

Done. I've written the full phasewise checklist with explicit passing criteria to:

      C:\Workspace\Akashic-Engine\BUILD_CHECKLIST.md

    Since you're starting fresh, I reframed the scope doc's "known bugs" (which referenced code that didn't exist in the empty repo) as "build correctly
    the first time" items, and pointed the salvage items at the real source: C:\Workspace\1Akashic-Engine (backend/frontend/agents + Knowledge OS + Note
    Refresher subfolders — I confirmed they're there).

    Here's the structure (each item in the file has a "> PASS:" testable condition):

    PHASE 0 — Security & hygiene (P0, blocking)
      - Secrets scaffold (.env never committed, .env.example + pydantic-settings)
      - Bearer-token auth on all routers (unauth -> 401)
      - CORS locked to localhost
      - Generated state (data/, chroma, .nicegui) gitignored
      - Rotate the leaked key in the OLD 1Akashic-Engine/.env (it's tracked there)

    PHASE 1 — Knowledge Graph (Pillar 1)
      - Read-only vault scanner (python-frontmatter, handles CRLF + fenced blocks, strips [[x|alias]])
      - Typed graph model + builder (nodes: concept/adr/project/person/tech; typed+weighted edges)
      - Orphan detection (degree==0)
      - Centrality (degree + betweenness via networkx)
      - Dependency graph (project -> prereq/depends_on)
      - Graph UI page with type filter + click-to-open

    PHASE 2 — Quality Scoring (Pillar 4)  [built before Recommend so it has inputs]
      - The 6 GOAL dimensions: Completeness, Freshness (deterministic from mtime+updated), Reusability, Connectedness (from graph), Confidence, Review-priority
      - Dimension mapping decision: old 8 dims (difficulty/importance/...) -> kept/merged/dropped; single source of truth

    PHASE 3 — Recommendation Engine (Pillar 2)
      - 4 morning questions, all score-driven
      - Stale-ADR detection fixed for NESTED folders (old _detect_adr_gaps only checked immediate parent)
      - Blocked-project detection via dependency graph
      - Promotion Reference->Curated ranking
      - Unified GET /daily-brief

    PHASE 4 — Agent Workspace (Pillar 3)
      - Shared context layer + dispatcher (port from Knowledge OS)
      - 5 agents: Career Architect (build — doesn't exist yet), Data Engineering Mentor, PKM Curator, Project Reviewer, Interview Coach
      - Tools: search_notes, get_note, get_neighbors, find_missing_prereqs, score_note, summarize_cluster
      - Agents UI page

    PHASE 5 — Merge & unify
      - Fold Note Refresher logic in (idempotent daily review + 14-day spaced repetition)
      - Retire Knowledge OS prototype; port dispatcher
      - Graph as single shared backbone
      - Single config.yaml + pydantic-settings + example files

    PHASE 6 — Bug-avoidance (real in 1Akashic-Engine)
      - 8 Akashic-Engine bugs + 5 Note Refresher bugs, each with a "> PASS:" that proves you didn't reintroduce it

    PHASE 7 — Cross-cutting (P2, throughout)
      - Tests (pytest, coverage gate), CI (ruff+mypy+pytest), pre-commit, Docker (Ollama sidecar + Chroma), performance (mtime skip, Chroma singleton,
    LLM cache), observability (/health + token cost in UI)

    Key assumptions baked in:
      - Vault taxonomy stays manual; scanner is read-only until you finish reviewing notes.
      - OpenRouter key added to .env later; LLM calls sit behind a client so graph/score layers run offline via Ollama.
      - 1Akashic-Engine is the salvage reference, not the target — copy patterns, not bugs.

    Want me to start executing Phase 0 + Phase 1 now (scaffold the Poetry/FastAPI/NiceGUI project and build the read-only scanner that actually parses
    your 135 notes), or would you rather adjust the checklist first?