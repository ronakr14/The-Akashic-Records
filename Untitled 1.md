Claude finished the response

## You said: help me understand this github repo: Fission-AI/OpenSpec: Spec-driven development (SDD) for AI coding assistants.

help me understand this github repo: [Fission-AI/OpenSpec: Spec-driven development (SDD) for AI coding assistants.]([https://github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)) and where I can use it

10:55 AM

## Claude responded: Good, I have a thorough picture now.

Searched the web

Searched the web

Good, I have a thorough picture now. Let me break this down clearly.

---

### OpenSpec — What It Actually Is

OpenSpec solves a specific, real problem: **AI coding assistants are stateless and context-hungry**. When your requirements only live in chat history, the AI drifts, hallucinates scope, and rebuilds what it shouldn't touch. OpenSpec adds a **lightweight spec layer on disk** — structured Markdown files that become the persistent ground truth your AI works from.

It's not a new language or a compiler. It's a **convention + CLI** that teaches AI assistants where to look before writing code.

---

#### The Core Mental Model

OpenSpec organizes work into two directories: `openspec/specs/` (source of truth — how your system currently behaves) and `openspec/changes/` (proposed modifications — each change gets its own folder with proposal, specs, design, and tasks). The separation means you can work on multiple changes in parallel without conflicts, and archive them cleanly when done. [github](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md)

The key insight is **delta specs**: rather than rewriting full specs for every change, you describe only what's `ADDED`, `MODIFIED`, or `REMOVED`. This makes it practical for brownfield codebases — which is most real work.

The lifecycle looks like:

```
/opsx:propose → artifacts generated → /opsx:apply → AI implements → /opsx:archive
```

On archive, deltas merge into the main specs, and the change folder moves to `archive/` with full context preserved (the "why" and "how" don't disappear).

---

#### Where You'd Actually Use This

Given your work across pipelines, RAG systems, and Snowflake-native tooling, here are the natural fits:

**1. Snowflake AI system design (high value)** When building Cortex RAG pipelines or multi-stage Snowpark workflows, the failure mode is usually "the AI rewrites the embedding layer when you asked it to fix chunking." OpenSpec gives you a `specs/retrieval/spec.md` with locked behavior contracts (embedding model, chunk strategy, vector search config) — the AI reads it before touching anything.

**2. Iterative pipeline development with Claude Code** OpenSpec works with 20+ AI assistants via slash commands, and the recommended models for planning and implementation are high-reasoning ones like Opus 4. For a multi-task Snowflake pipeline (streams → tasks → dynamic tables), you'd spec each stage's contract, then `/opsx:apply` one stage at a time. The AI doesn't cross-contaminate stages because the spec boundaries are explicit. [github](https://github.com/Fission-AI/OpenSpec)

**3. Interview tooling / hiring artifacts** You've been building structured interview frameworks. OpenSpec is a natural fit here too — you could version-control your interview rubrics, scenario banks, and evaluation matrices as OpenSpec specs. When a role changes or the stack evolves, you cut a `change/` against it rather than rewriting from scratch.

**4. Brownfield governance layer work** When adding Row Access Policies or Dynamic Data Masking to existing Snowflake tables, the risk is an AI that "helpfully" refactors the underlying table structure. A delta spec scoped to only the governance behavior prevents that.

---

#### What It's Not

It's not a test framework, not a linter, and not an agent platform. It's purely a **context-engineering convention** — structured Markdown that makes AI assistants less wrong by giving them bounded, versioned requirements to work from.

The closest analogy: it's what a good `ARCHITECTURE.md` tries to be, but formalized, versioned, and with AI-native slash commands built in.

---

**Worth trying if:** you're using Claude Code or Cursor on anything with multiple moving parts and have felt the pain of the AI "re-solving" something you'd already decided. That's exactly the gap this fills.

## You said: how its different from Fission-AI/OpenSpec: Spec-driven development (SDD) for AI coding assistants.

how its different from [Fission-AI/OpenSpec: Spec-driven development (SDD) for AI coding assistants.]([https://github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec))

10:58 AM

## Claude responded: Could you clarify what you're comparing OpenSpec to?

Could you clarify what you're comparing OpenSpec _to_? It looks like the link you pasted points back to OpenSpec itself — were you thinking of a different tool, like:

- **Kiro** (AWS's IDE with spec-driven features)
- **Spec Kit** (GitHub's spec framework)
- **Claude's built-in memory/projects**
- **Something else entirely**

Which comparison did you have in mind?

## You said: I meant github/spec-kit: 💫 Toolkit to help you get started with Spec-Driven Development

I meant [github/spec-kit: 💫 Toolkit to help you get started with Spec-Driven Development]([https://github.com/github/spec-kit](https://github.com/github/spec-kit))

10:58 AM

## Claude responded: Good comparison to make — they're solving the same problem from very different angles.

Fetched: GitHub - github/spec-kit: 💫 Toolkit to help you get started with Spec-Driven Development

Fetched: GitHub - github/spec-kit: 💫 Toolkit to help you get started with Spec-Driven Development

Good comparison to make — they're solving the same problem from very different angles. Here's the breakdown:

---

### The Core Philosophical Split

**Spec Kit** (GitHub) treats specs as a **generation source** — you write rich specs and the AI derives code from them. The flow is predominantly top-down: spec → plan → tasks → implement.

**OpenSpec** treats specs as a **persistent ground truth** — you use them to bound what the AI is allowed to touch, especially on existing codebases. The flow is delta-driven: what changed, why, and where does it land in the source of truth.

This difference in framing cascades into almost everything else.

---

### Side-by-Side Breakdown

|Dimension|Spec Kit (GitHub)|OpenSpec (Fission-AI)|
|---|---|---|
|**Primary target**|Greenfield / new features from scratch|Brownfield / iterative changes on existing systems|
|**Spec model**|Full specs per feature (whole-doc)|Delta specs — only ADDED / MODIFIED / REMOVED|
|**Workflow structure**|Linear phases with gates: constitution → specify → plan → tasks → implement|Fluid, no phase gates — create any artifact in any order|
|**Setup weight**|Heavier: Python/uv, templates, constitution, scripts|Lighter: `npm install -g`, `openspec init`|
|**Runtime**|Python CLI (`specify`)|Node.js CLI (`openspec`)|
|**AI integration model**|Slash commands that trigger multi-step agent workflows|Slash commands that read/write spec files as context|
|**Spec lifecycle**|Per-feature `.specify/specs/001-feature/` directories, not merged back|Changes archive and delta-merge into a living `openspec/specs/` source of truth|
|**Customization**|Extensions (new capabilities) + Presets (format overrides) — community catalog|Custom schemas (artifact dependency graphs)|
|**Constitution/principles**|Explicit first step (`/speckit.constitution`) — governs all downstream decisions|Not a named concept — project context lives in specs themselves|
|**Verification**|`/speckit.analyze` for cross-artifact consistency|`/opsx:verify` checks implementation against specs|
|**Parallel work**|One feature branch at a time, sequential|Multiple `changes/` folders can coexist without conflict|

---

### The Key Structural Difference: How Specs Evolve

This is where the real divergence is.

**Spec Kit** produces specs per-feature in numbered folders (`specs/001-create-taskify/`). After running `/speckit.specify`, you get a new branch created and a specification in the `specs/001-create-taskify` directory. These specs don't merge into a unified system description — each feature's spec is standalone. [github](https://github.com/github/spec-kit)

**OpenSpec** maintains a rolling `openspec/specs/` directory as the source of truth for how the _entire_ system currently behaves. Each change proposes deltas against it, and on archive those deltas merge in. The next change builds on top of that merged state. It's closer to how a schema migration system works — the spec is versioned state, not just documentation.

For brownfield data systems (which is most of what you work with), OpenSpec's model maps more naturally to how systems actually evolve: you're not rebuilding the retrieval pipeline, you're modifying the chunk overlap and adding a reranker. A delta spec for that is precise. A full spec would be noise.

---

### Which to Use When

**Reach for Spec Kit when:**

- You're building something net-new (a new Snowpark pipeline stage, a new Cortex RAG endpoint)
- You want a constitution layer — explicit governing principles baked in before any code is written
- You want richer research/planning artifacts (`research.md`, `data-model.md`, `api-spec.json`)
- You're on a team that wants the full waterfall-like artifact trail

**Reach for OpenSpec when:**

- You're modifying existing systems (adding governance to live tables, tuning embedding behavior, changing task schedules)
- You need multiple changes in-flight simultaneously without branch conflicts
- You want minimal ceremony — initialize in one command and start speccing
- You want the spec to remain the living system description, not just a per-feature artifact

---

### The Honest Tradeoff

Spec Kit is more thorough on greenfield but heavier to maintain on a codebase that's already moving. OpenSpec is more surgical but assumes you already have context about what the system does — it won't help you reason about a system from scratch as well as Spec Kit will.

For your Snowflake work specifically: the delta model in OpenSpec maps cleanly to how Snowflake-native systems evolve (Cortex tuning, Stream/Task topology changes, governance layering). Spec Kit would be the better pick if you're standing up something like a net-new Cortex RAG pipeline from scratch and want structured research + planning artifacts before a line of SQL gets written.