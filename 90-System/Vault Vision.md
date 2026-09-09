---
domain: pkm
subdomain: vault-design
note_type: architecture
source_type: self
status: curated
level: advanced
---
# The Akashic Records

> A local-first Personal Knowledge Management system evolving into a **Career Operating System and Personal Knowledge Intelligence Engine**.

The Akashic Records is a personal knowledge repository designed to capture, develop, connect, and continuously improve knowledge.

It is built around a simple idea:

> **Knowledge should not merely be stored. It should help determine what to learn, what to improve, what to build, and what to create next.**

The repository currently uses **Obsidian and Markdown** as the primary human-facing interface, with Git providing version history and an evolving intelligence layer providing automation, analysis, and recommendations.

---

## Vision

The long-term goal is to evolve the repository into:

**80% Career Operating System + 20% External Brain**

The system should eventually understand the relationship between:

- Knowledge
    
- Projects
    
- Career goals
    
- Learning history
    
- Experiments
    
- Technical decisions
    
- Writing
    
- Tasks
    
- Concepts and technologies
    

and provide useful recommendations such as:

> What should I learn today?

> Which notes need attention?

> Which concepts are poorly connected?

> What topics am I weak in?

> What should I write about?

> Which project is missing prerequisite knowledge?

The ultimate destination is an **intelligent personal knowledge graph** capable of reasoning over the user's accumulated knowledge and career development.

---

# Core Philosophy

The repository follows five primary principles.

### 1. Folders provide context

Folders answer:

> **Where does this knowledge belong?**

They should remain relatively shallow and topic-centric.

### 2. Metadata provides classification

Frontmatter answers:

> **What is this note?**

A concept, technology, project, experiment, ADR, career note, etc. should be represented through metadata rather than unnecessary folder hierarchies.

### 3. Links provide relationships

Links answer:

> **How does this knowledge connect to other knowledge?**

The eventual knowledge graph will rely heavily on these relationships.

### 4. Automation provides attention

Automation should answer:

> **What deserves my attention?**

This includes identifying stale, incomplete, weakly connected, or high-value knowledge.

### 5. AI provides intelligence

AI should eventually answer:

> **What should I do next?**

AI should initially **suggest rather than autonomously modify important knowledge**. Human approval remains part of the curation process.

---

# Repository Structure

The repository is organized primarily by **topic and context**, rather than by note type.

```text
The-Akashic-Records/
│
├── 00-Daily/
│
├── 01-Knowledge/
│   ├── AI & LLM/
│   ├── Architecture/
│   ├── Cloud/
│   ├── Data Engineering/
│   ├── Databases/
│   ├── PKM/
│   ├── Python/
│   └── Software Engineering/
│
├── 02-Projects/
│
├── 03-Career/
│   ├── Career/
│   ├── Interview/
│   └── System Design/
│
├── 04-Writing/
│   ├── Ideas/
│   ├── Drafts/
│   └── Published/
│
├── 05-Decisions/
│
├── 06-Experiments/
│
├── 07-Personal/
│
├── 08-Prompts/
│
├── 90-System/
│
└── 99-Archive/
```

The exact structure may evolve as the system matures.

The important rule is:

> **Do not create folders merely because a new note type exists.**

For example, Concepts, Technologies, and Tools do not necessarily require separate top-level folders. They can be represented through note metadata while remaining within their relevant domain.

---

# Daily Notes

Daily Notes are the primary **capture mechanism**.

They can contain:

- Daily planning
    
- Work and learning logs
    
- Temporary notes
    
- Ideas
    
- Observations
    
- Tasks
    
- Potential knowledge candidates
    

The intended workflow is:

```text
Capture
   ↓
Daily Note
   ↓
Develop / Review
   ↓
Promote when valuable
   ↓
Permanent Knowledge
```

The repository intentionally does **not** maintain a separate Inbox by default.

The assumption is:

> **If something does not yet have a home, today's Daily Note is its temporary home.**

Automation may later identify candidates for promotion, but the user approves important changes.

New daily notes are created from `90-System/templates/Daily Note.md` (Log / Learned / Ideas / Tasks / Promote sections).

AI-generated tech briefings are a separate feed, not capture. They live in `00-Daily/Briefings/` and are mined for recurring themes in `00-Daily/Briefings/_Briefings Index.md`, which links them back into the knowledge graph.

---

# Knowledge

Knowledge is organized primarily by domain and topic.

For example:

```text
01-Knowledge/
└── Data Engineering/
    └── Apache Spark/
        ├── Apache Spark.md
        ├── Spark Architecture.md
        ├── Spark AQE.md
        ├── Spark Shuffle.md
        └── Spark Performance.md
```

A note's type is determined through metadata.

For example:

```yaml
note_type: concept
```

or:

```yaml
note_type: technology
```

or:

```yaml
note_type: tool
```

This avoids duplicating the same knowledge across Concepts, Technologies, Tools, Tutorials, and similar folders.

---

# Projects

Projects are where knowledge is **applied**.

Project-specific information belongs with the project.

Reusable knowledge should eventually be promoted into the main Knowledge area.

The intended lifecycle is:

```text
Project Research
      ↓
Experiment / Investigation
      ↓
Reusable Insight
      ↓
Knowledge
      ↓
Curated Knowledge
      ↓
Evergreen Knowledge
```

Projects therefore act as consumers and producers of knowledge.

---

# Career

Career development is a first-class part of the repository.

Career-related areas include:

```text
03-Career/
├── Career/
├── Interview/
└── System Design/
```

Career notes should generally reference existing technical knowledge instead of duplicating it.

For example:

```text
Interview/Spark Interview Questions.md
```

can reference:

```text
Knowledge/Data Engineering/Apache Spark/Spark Shuffle.md
```

This allows interview preparation to become a **view over knowledge**, rather than another independent knowledge base.

---

# Writing

Writing is treated as a downstream consumer of accumulated knowledge.

```text
04-Writing/
├── Ideas/
├── Drafts/
└── Published/
```

The long-term goal is to identify writing opportunities from knowledge already present in the repository.

For example:

```text
Connected Knowledge
        ↓
Interesting Knowledge Cluster
        ↓
Potential Article
        ↓
Writing Idea
        ↓
Draft
        ↓
Published
```

This supports the question:

> **What should I write about?**

without relying entirely on externally generated topic lists.

---

# Decisions

Architectural and important personal decisions are maintained separately:

```text
05-Decisions/
```

These are represented through ADR-style notes.

The distinction is intentional:

> **Knowledge describes what is known.**

> **Decisions describe what was chosen and why.**

Decisions may reference concepts, technologies, projects, constraints, and alternatives.

---

# Experiments

Experiments provide a structured place for testing ideas.

```text
06-Experiments/
```

A typical experiment can follow:

```text
Hypothesis
    ↓
Implementation
    ↓
Observation
    ↓
Result
    ↓
Conclusion
    ↓
Knowledge / Decision
```

This is particularly useful for technical experiments involving data engineering, AI/LLMs, software architecture, databases, and PKM tooling.

---

# Task Management

Tasks are intentionally **not stored in a dedicated `Tasks/` folder**.

Tasks should normally remain where their context exists:

```text
Daily Note
    └── Task

Project
    └── Task

Knowledge Note
    └── Task

Career Note
    └── Task

Writing Note
    └── Task
```

The desired model is:

> **Centralized task visibility without centralized task storage.**

A task can therefore be discovered globally while retaining its original context.

No task plugin is adopted yet (Operon was evaluated and rejected 2026-09-09). Tasks stay as plain Markdown checkboxes in their context notes until a plugin earns its place.

The desired task system should provide:

- One global task view
    
- Tasks from anywhere in the vault
    
- Scheduling
    
- Due dates
    
- Reminders
    
- Recurring tasks
    
- Rescheduling/postponement
    
- Mobile support
    
- Task identity
    
- Inline and larger file-based tasks
    

An important design principle is to **reschedule persistent tasks rather than repeatedly duplicate unfinished tasks into Daily Notes**.

---

# Metadata

Metadata is a core part of the system.

The repository uses structured frontmatter to describe notes independently from their physical location.

Typical dimensions include:

- Domain
    
- Subdomain
    
- Note type
    
- Source
    
- Status
    
- Level
    
- Confidence
    
- Completeness
    
- Importance
    
- Career relevance
    

The metadata model is expected to evolve as the intelligence layer becomes more sophisticated.

However:

> **Metadata should be added because the system has a use for it, not simply because it might be useful someday.**

---

# Knowledge Quality

Knowledge quality is evaluated across multiple dimensions.

Current areas include concepts such as:

- Confidence
    
- Completeness
    
- Importance
    
- Career relevance
    
- Connectedness
    
- Freshness
    

The system is intended to identify knowledge that is:

- Incomplete
    
- Unverified
    
- Stale
    
- Poorly connected
    
- Missing metadata
    
- Important but underdeveloped
    

A detailed knowledge-maturity model may be introduced later, but it is intentionally not a current priority.

---

# Intelligence Layer

The long-term architecture includes an intelligence layer that reasons over the repository.

Conceptually:

```text
                         Career Goals
                              │
                              ↓
Daily Notes ─────────→ Knowledge Graph ←──────── Projects
                              ↑
                              │
                         Experiments
                              │
                              ↓
                 Akashic Intelligence Engine
                              │
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
         Learn Next      Review Next      Write Next
```

The intelligence layer should eventually support:

### Learning recommendations

Identify what should be learned based on:

- Career relevance
    
- Knowledge gaps
    
- Project requirements
    
- Importance
    
- Freshness
    
- Prerequisites
    
- Previous learning
    

### Knowledge maintenance

Identify:

- Stale notes
    
- Incomplete notes
    
- Weakly connected concepts
    
- Broken links
    
- Missing metadata
    
- Knowledge requiring verification
    

### Writing recommendations

Identify:

- Strong knowledge clusters
    
- Interesting connections
    
- Underexplored topics
    
- High-value technical ideas
    
- Potential articles
    

### Career intelligence

Connect:

- Career goals
    
- Projects
    
- Knowledge
    
- Experiments
    
- Architecture decisions
    
- Technical writing
    
- Interview preparation
    

to provide a broader picture of career development.

---

# Automation Philosophy

Automation is a major part of the long-term system.

However, automation should generally follow:

```text
Detect
  ↓
Analyze
  ↓
Suggest
  ↓
Human approval
  ↓
Apply
```

rather than:

```text
Detect
  ↓
AI changes everything
```

The system should remain understandable, inspectable, and recoverable.

Git provides an additional safety layer by preserving repository history.

---

# Current Technology Direction

The repository is designed around a local-first and developer-oriented workflow.

Primary components include:

- Markdown
    
- Obsidian
    
- Git
    
- Python
    
- Structured frontmatter
    
- Dataview
    
- Obsidian Bases
    
- SQLite / local data stores where appropriate
    
- Embeddings / semantic search where useful
    
- AI / LLM-based analysis
    
- Knowledge graph techniques
    

The architecture should remain modular so individual components can be replaced without rebuilding the entire system.

---

# Design Principles

### Local-first

The repository should remain usable as a collection of Markdown files without requiring a hosted SaaS platform.

### Human-readable

Important information should remain understandable without the intelligence layer.

### Git-friendly

Changes should remain trackable and recoverable.

### Metadata-driven

Classification should not depend excessively on folder structure.

### Link-rich

Relationships between concepts are first-class information.

### Automation-assisted

Automation should reduce maintenance rather than create additional maintenance.

### AI-assisted, not AI-dependent

The repository should remain useful even if AI services are unavailable.

### Progressive complexity

Start simple and introduce complexity only when there is a demonstrated need.

---

# Roadmap

The system is intended to evolve incrementally.

## Phase 1 — Foundation

- Normalize folder structure
    
- Normalize frontmatter
    
- Establish note types
    
- Improve Daily Notes
    
- Establish task architecture
    
- Improve links
    
- Clean existing notes
    
- Strengthen quality scoring
    

## Phase 2 — Knowledge Intelligence

- Automated note classification
    
- Link analysis
    
- Broken-link detection
    
- Orphan detection
    
- Knowledge quality scoring
    
- Freshness analysis
    
- Duplicate detection
    
- Knowledge gap detection
    

## Phase 3 — Knowledge Graph

- Concept relationships
    
- Technology relationships
    
- Project dependencies
    
- ADR relationships
    
- Prerequisite discovery
    
- Graph-based recommendations
    

## Phase 4 — Intelligence Engine

- Learning recommendations
    
- Review recommendations
    
- Writing recommendations
    
- Career recommendations
    
- Project knowledge-gap detection
    
- Personalized daily review
    

## Phase 5 — Agent Workspace

Potential specialized agents:

```text
Career Architect
Data Engineering Mentor
PKM Curator
Project Reviewer
Interview Coach
Writing Advisor
```

All agents should reason over the same underlying repository rather than creating separate knowledge silos.

---

# What This Repository Is Not

The Akashic Records is intentionally **not**:

- Just a note-taking application
    
- A folder-organizing exercise
    
- A replacement for every productivity application
    
- A giant task database
    
- An autonomous AI knowledge base
    
- A collection of disconnected summaries
    
- A system that requires every piece of information to be perfectly classified immediately
    

The goal is not organizational perfection.

The goal is to build a system that **gets more useful as knowledge accumulates**.

---

# Long-Term Vision

The ideal end state is a system where the user can open the repository and ask:

```text
What should I learn today?

What am I weak at?

What knowledge needs attention?

What concepts are poorly connected?

What project is blocked by missing knowledge?

What have I learned recently?

What should I write about?

Which architectural decisions are becoming stale?

What should I work on next?
```

And instead of returning generic productivity advice, the system answers using the user's **actual knowledge, projects, history, goals, and work**.

That is the purpose of **The Akashic Records**.

> **Capture knowledge. Connect it. Apply it. Improve it. Let it guide what comes next.**