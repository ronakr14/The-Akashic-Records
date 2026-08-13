---
tags:
  - agents
  - agent-compiler
  - mcp
  - code-generation
  - llm
  - rag
  - architecture
  - github/inbox/advance
---
```table-of-contents
title: 
style: nestedList # TOC style (nestedList|nestedOrderedList|inlineFirstLevel)
minLevel: 0 # Include headings from the specified level
maxLevel: 0 # Include headings up to the specified level
include: 
exclude: 
includeLinks: true # Make headings clickable
hideWhenEmpty: false # Hide TOC if no headings are found
debugInConsole: false # Print debug info in Obsidian console
```

# AI Summary

AgentHatch is an agent compiler that treats `SKILL.md` as source code rather than a runtime prompt. Its core architecture separates deterministic parsing, multi-pass LLM inference, a structured intermediate representation ([[AHSSPEC]]), validation, code generation, and runtime execution. The key architectural idea is the compiler boundary: probabilistic LLM inference transforms prose into a typed specification, after which conventional software-engineering mechanisms can validate, generate, test, package, and execute the resulting agent. Current releases also include post-generation repair, subprocess sandboxing, MCP integration, context compaction, and knowledge-base/RAG capabilities. It is a useful architectural reference, but not something to adopt wholesale.

# AgentHatch

## 1. What It Is

[AgentHatch](https://github.com/agenthatch/agenthatch) is a compiler-like framework for turning a `SKILL.md` into a standalone, runnable Python agent.

The central thesis is simple:

> A skill should be treated more like source code than like a prompt.

```text
SKILL.md
   ↓
Deterministic Parse
   ↓
ContextPack
   ↓
6 specialized LLM harnesses
   ↓
AHSSPEC
   ↓
Validation / normalization
   ↓
Jinja2 code generation
   ↓
Standalone Python agent
   ↓
Runtime + tools + MCP + knowledge + state machine
```

The important shift is from **runtime prompt interpretation** to **compile-time agent construction**.

---

## 2. Problem Being Solved

AgentHatch targets weaknesses in raw `SKILL.md` systems:

- skills can leak instructions into one another through shared context
- long skills are treated as loose reference material rather than contracts
- every active skill consumes context space
- tool interfaces are expressed as prose rather than typed contracts
- ambiguities and tool-definition errors are discovered late
- scaling from a few skills to many becomes difficult without isolation and indexing

The deeper problem is not Markdown. It is the lack of a **compilation and validation boundary**.

```text
Raw skill system
Human prose → LLM interpretation → runtime behavior

AgentHatch
Human prose → structured specification → generated software → runtime behavior
```

---

## 3. Architecture

### 3.1 Phase 1 — Deterministic Parse

Phase 1 performs no semantic AI interpretation. The implementation builds a `ContextPack` containing frontmatter, Markdown body, file manifest, file hashes, readable contents, entrypoint information and parse warnings.

`FileEntry` records relative path, SHA-256 hash, size and content. This deliberately separates filesystem facts from semantic interpretation.

```text
Filesystem facts ──────────────► deterministic layer
Meaning / intent / interfaces ─► LLM layer
```

This is one of the strongest design choices in the project.

### 3.2 Phase 2 — Six-Harness LLM Pipeline

The current implementation defines six specialized harnesses:

| Harness | Responsibility |
|---|---|
| A — Identity | Extract identity, name, version and description |
| B — Intent | Infer triggers and user intents |
| C — Interface | Infer capabilities, parameters and return schemas |
| D — Base | Detect runtime/base class and instruction structure |
| E — Assembly | Cross-validate and assemble the unified specification |
| F — MCP | Infer MCP server connections |

Harnesses use bounded Analyze → Infer → Self-Validate → Correct loops and expose confidence, retries and token-usage information.

The architectural lesson is more important than the exact six roles:

> Large ambiguous LLM tasks can be decomposed into smaller inference contracts that are independently validated and then assembled.

### 3.3 AHSSPEC — Intermediate Representation

`AHSSPEC` is the most important architectural concept in AgentHatch.

The current implementation defines an AHS v1.1 Pydantic specification containing concepts such as:

- identity
- intent
- capabilities
- input/output schemas
- requirements
- MCP servers
- API templates
- environment variables
- workflow steps
- safety rules
- runtime/base configuration
- dependencies
- resources
- composition/event listeners
- confidence information

Conceptually:

```text
SKILL.md → ContextPack → LLM inference → AHSSPEC → generated agent
```

AHSSPEC is effectively an **intermediate representation (IR)** between natural-language intent and executable software.

Without an IR:

```text
LLM → code
```

With an IR:

```text
LLM → structured contract → validation → code
```

The second architecture creates a proper place for validation, auditing, versioning, diffing, policy enforcement and deterministic generation.

### 3.4 Defensive Schema Handling

The schema layer explicitly handles common LLM mistakes such as strings where lists are expected, invalid runtime values, numeric timeouts, malformed dependency/environment structures and invalid identity values.

This reinforces an important principle:

> **Structured LLM output is still probabilistic input and needs defensive validation.**

Pydantic supplies the contract; coercion attempts to recover predictable model formatting mistakes before rejecting the result.

---

## 4. Code Generation

Jinja2 templates convert AHSSPEC into a standalone Python package containing artifacts such as:

```text
hatched-agent/
├── pyproject.toml
├── runtime.toml
├── README.md
├── agenthatch.yaml
└── src/<package_name>/
    ├── __init__.py
    ├── agent.py
    ├── tools.py
    └── references.py
```

The output can be inspected, tested, packaged, versioned and debugged using conventional software-engineering workflows.

That makes the generated agent a **software supply-chain artifact**, which is both a strength and a new security concern.

---

## 5. Post-Generation Self-Review

After generation, AgentHatch can inspect `tools.py`, execute tools with mock parameters and repair detected defects for a bounded number of rounds.

```text
Generate → Inspect → Test → Repair → Inspect
```

The review targets issues such as undefined variables, `None` attribute failures, semantic stubs, runtime failures and exception-swallowing patterns.

This should not be confused with formal verification. It is better described as:

> **LLM-generated code + automated checks + bounded LLM repair.**

The approach improves practical reliability but does not prove correctness.

---

## 6. Runtime — PlanLayer

Generated agents use a six-state planning model:

```text
STARTING
   ↓
PLANNING
   ↓
EXECUTING
   ↓
VERIFYING
   ↓
REPLANNING ──┐
   └─────────┘
   ↓
DONE
```

The runtime can adapt to failures, merge completed steps and handle tool timeouts.

The architectural significance is that the LLM is not the whole execution engine:

```text
LLM reasoning
    ↓
Plan / intent
    ↓
Runtime state machine
    ↓
Tool execution
    ↓
Verification
    ↓
Replanning when necessary
```

This creates explicit control points for retries, timeouts, observability and policy enforcement.

---

## 7. MCP as a Compiled Capability

MCP is represented in AHSSPEC through structured server definitions. Harness F detects MCP servers and Harness E incorporates them into the assembled interface.

```text
SKILL.md
   ↓
MCP detection
   ↓
MCPServerEntry
   ↓
AHSSPEC
   ↓
Generated runtime configuration
   ↓
MCP tools
```

The benefit is less manual wiring. The risk is an expanded trust boundary.

A mature implementation needs explicit answers to:

- Which tools are allowed?
- Who authorizes them?
- Can a skill request excessive permissions?
- How are MCP credentials isolated?
- Can untrusted skills cause unsafe connections?
- Are tool capabilities represented as policy objects?

Automatic tool discovery is therefore a security-sensitive compilation output, not merely a convenience feature.

---

## 8. Sandbox and Security

The project includes a subprocess sandbox with command-whitelist tiers in `agenthatch-core`. Its roadmap identifies Docker-backed isolation as a future improvement for stronger filesystem and network isolation.

This matters because AgentHatch combines:

```text
LLM-derived specification
        ↓
Generated executable code
        ↓
Tool / MCP access
        ↓
External side effects
```

A subprocess whitelist is useful containment, but it is not equivalent to a hardened container or VM boundary.

For production use, stronger isolation, capability-based permissions, secret isolation and network policy would be important.

---

## 9. Knowledge / RAG Layer

AgentHatch has evolved beyond pure agent generation. The v1.0 line introduced knowledge-backed agents through `KnowledgeBaseBrick`.

The current direction includes:

- SQLite FTS5
- BM25 keyword retrieval
- generated `retrieve()` functionality
- skill-derived retrieval configuration
- optional semantic search
- runtime knowledge-base integration

```text
Skill + knowledge files
        ↓
     Hatch time
        ↓
Knowledge-base artifact
        ↓
Generated retrieve()
        ↓
Runtime query
        ↓
BM25 / optional embeddings
        ↓
Relevant references
        ↓
Agent response
```

This is interesting because the compiler is no longer compiling only **behavior**. It is also compiling **knowledge-access behavior**.

Current roadmap gaps include LLM reranking, shared cross-agent KB memory and automated stale-entry maintenance.

---

## 10. Current Capabilities

The project currently documents these capabilities:

- 6-harness LLM pipeline with self-validation
- AHSSPEC structured specification
- MCP auto-detection
- PlanLayer state machine
- context auto-compaction
- subprocess sandbox with command whitelist
- hatch reports in human-readable and JSON forms
- post-generation inspect/test/repair loop
- SQLite FTS5 + BM25 knowledge retrieval
- optional semantic retrieval
- confidence scoring and retry penalties
- JSON Schema constraint mapping to Pydantic types
- exception-swallow antipattern detection
- skillhouse indexing and management

The CLI includes operations such as `init`, `skills add/list/delete`, `hatch`, `run`, `search`, `doctor` and `assemble`.

---

## 11. The Real Architectural Differentiator

The important idea is not "generate an agent from Markdown." The important idea is the **compiler boundary**.

```text
Human-authored intent
        ↓
Probabilistic interpretation
        ↓
Structured intermediate representation
        ↓
Validation / normalization
        ↓
Code generation
        ↓
Executable artifact
        ↓
Controlled runtime
```

This creates a useful separation of responsibility:

| Concern | Preferred mechanism |
|---|---|
| Natural-language interpretation | LLM |
| Schema validation | Conventional code |
| Type checking | Conventional code |
| Policy validation | Conventional code |
| Code generation | Templates / compiler |
| Runtime state | Deterministic state machine |
| Tool execution | Runtime |
| Semantic reasoning | LLM |
| Artifact packaging | Conventional tooling |

This is the main idea worth preserving from the project.

---
## 12. Architecture Tradeoffs

AgentHatch makes several deliberate tradeoffs. The compiler model improves structure and governance opportunities, but it also introduces a build lifecycle that simpler agent frameworks do not need.

| Decision | Benefit | Cost / Risk |
|---|---|---|
| Compile skills into agents | Better isolation, inspectable artifacts, conventional testing | Build step, generated-code lifecycle, artifact drift |
| Use AHSSPEC as an IR | Validation, diffing, policy enforcement and multiple generation targets become possible | Another schema that must evolve and remain backward-compatible |
| Multiple LLM harnesses | Smaller reasoning problems, targeted retries and better diagnostics | More inference calls, latency, token cost and orchestration complexity |
| Generate Python | Easy integration with the Python ecosystem | Python becomes a runtime constraint and generated code becomes a supply-chain concern |
| Explicit PlanLayer | Better control over retries, timeouts and verification | More runtime machinery and state-management complexity |
| Infer MCP configuration | Less manual wiring | Tool discovery becomes part of the security boundary |
| Post-generation LLM repair | Can recover from common generated-code defects | Repair can introduce new defects; still not verification |
| Compile knowledge access | Makes retrieval a first-class capability | Knowledge freshness, indexing and rebuild lifecycle become compiler concerns |
| Skill composition | Enables larger agent systems | Dependency, capability, authorization and conflict resolution become much harder |

The core tradeoff is:

> **AgentHatch exchanges runtime simplicity for build-time structure and control.**

That is a reasonable trade for governed agent systems, but unnecessary overhead for a small one-off agent.

---

## 13. What AgentHatch Gets Right

### Deterministic and probabilistic work are separated

The parser does not ask an LLM to rediscover filesystem facts.

### Specialized inference passes

Large ambiguous tasks are decomposed into smaller contracts that can be independently validated and retried.

### Intermediate representation

AHSSPEC gives the system a stable boundary between inference and generation.

### Generated artifacts are real software

The output can use ordinary debugging, testing, packaging and CI practices.

### Runtime state is explicit

PlanLayer provides control points that are missing from unconstrained agent loops.

### Failure handling is first-class

Schema coercion, retry penalties, confidence, post-generation inspection and bounded repair acknowledge LLM unreliability.

### Knowledge is becoming a compiled capability

The KB layer extends the compiler from behavior into retrieval and knowledge access.

---

## 14. What Needs Improvement

### Reproducibility is still conditional

Low-temperature inference and schema validation improve repeatability, but LLM inference remains probabilistic.

```text
Same input → likely similar output
```

is not equivalent to:

```text
Same input → identical artifact
```

A stronger build manifest should record provider, model/version, temperature, prompt/schema versions, source hashes and dependency versions.

### Security needs a stronger boundary

LLM-generated executable code plus MCP connectivity is a serious trust boundary. Docker isolation, capability permissions, secret isolation and network policies should be considered baseline for untrusted workloads.

### Observability is incomplete

Useful production signals would include per-harness latency, token/cost accounting, repair diffs, artifact lineage, tool traces, state transitions, retrieval quality, retry/failure metrics and policy violations.

### Self-review is not verification

Generated code should still pass conventional tests, static analysis, dependency scanning and explicit policy checks for higher-risk workloads.

### Artifact governance needs to mature

A production system should answer:

```text
Which skill version produced this agent?
Which model produced AHSSPEC?
Which schema/prompt version was used?
Which dependencies were installed?
Which MCP servers were authorized?
Can the artifact be rebuilt?
Can two builds be meaningfully diffed?
```

### Composition is substantially harder than single-skill compilation

Skill fusion and meta-agents introduce capability conflicts, dependency resolution, authorization conflicts, shared state and failure propagation. A stronger capability/dependency graph will be required for this to scale safely.

---
## 15. Enterprise Readiness Scorecard

| Dimension | Assessment | Why |
|---|---|---|
| Architecture | **Strong** | Clear separation between parsing, inference, IR, generation and runtime |
| LLM reliability | **Moderate** | Multi-pass validation helps, but the semantic layer remains probabilistic |
| Security | **Weak–Moderate** | Generated code and MCP access create a significant trust boundary |
| Sandbox | **Moderate** | Subprocess containment exists; stronger container isolation is still important |
| Observability | **Moderate** | Reports and usage information exist, but deeper runtime telemetry is needed |
| Testing | **Moderate** | Post-generation inspection/testing exists; it is not equivalent to comprehensive verification |
| Reproducibility | **Moderate** | Structured compilation helps, but model/provider changes can affect output |
| Governance | **Weak–Moderate** | Artifact lineage, authorization and policy lifecycle need more maturity |
| Deployment | **Moderate–Strong** | Generated Python packages fit conventional deployment workflows |
| Extensibility | **Strong** | The IR provides a useful extension boundary |
| Composition | **Immature** | Skill fusion introduces dependency, capability and authorization conflicts |
| Enterprise readiness | **Not yet** | The architecture is promising, but operational and security controls need more maturity |

### Bottom line

AgentHatch looks more like **promising agent-platform infrastructure** than a finished enterprise agent platform.

Its strongest enterprise property is the compiler boundary. Its largest enterprise gap is the governance and security lifecycle around generated artifacts and external capabilities.

---
## 16. Comparison With Adjacent Agent Architectures

AgentHatch should not be evaluated as simply another agent runtime. Its distinctive position is closer to an **agent compiler**.

| Architecture | Primary abstraction | Where it is strongest | AgentHatch difference |
|---|---|---|---|
| Raw `SKILL.md` systems | Prompt/instruction bundle | Simple reusable behavior | Compiles the skill into a structured artifact instead of interpreting it only at runtime |
| LangGraph-style orchestration | Graph/stateful execution | Explicit workflows, state and branching | Focuses earlier in the lifecycle: compiling a skill into an executable agent |
| OpenAI Agents SDK-style runtimes | Agent + tools + handoffs | Building and running agent applications | Adds a compilation/IR layer between authoring and runtime |
| CrewAI-style multi-agent frameworks | Roles/tasks/agent collaboration | Multi-agent orchestration | More concerned with constructing the individual agent artifact |
| AutoGen-style agent systems | Conversational/multi-agent interaction | Agent-to-agent workflows | Emphasizes deterministic build structure and generated artifacts |
| MCP-native agent architectures | Tool/resource interoperability | Standardized external capabilities | Treats MCP configuration as something that can be inferred and compiled into the agent |
| Traditional compiler / DSL architecture | Source → IR → artifact | Reproducible transformation and tooling | Applies the same architectural pattern while retaining probabilistic LLM inference |

### The architectural distinction

Most agent frameworks primarily answer:

> **How should an agent execute?**

AgentHatch is trying to answer:

> **How should an agent be compiled from a declarative specification?**

That gives AgentHatch a different lifecycle:

```text
Traditional agent framework

Author → Configure → Run → Observe

AgentHatch

Author skill
    ↓
Compile
    ↓
Validate
    ↓
Generate artifact
    ↓
Test / repair
    ↓
Package
    ↓
Run
    ↓
Observe
```

This makes build-time concerns first-class:

- schema evolution
- artifact versioning
- provenance
- reproducibility
- generated-code review
- policy enforcement
- dependency resolution
- incremental rebuilds

The downside is equally important: a compiler lifecycle adds complexity that a lightweight runtime-only agent may not need.

### Architectural positioning

```text
                    Runtime orchestration
                           ↑
          LangGraph / Agents SDK / CrewAI / AutoGen
                           │
                           │
                     AgentHatch
                           │
                           ↓
                Agent compilation layer
                           │
                           ↓
                 Compiler / DSL model
```

AgentHatch therefore sits between **agent runtime frameworks** and **compiler/DSL systems**.

That is the most useful way to position it in a technical landscape.

---

## 17. Lessons Worth Reusing

### 1. Introduce an intermediate representation

Do not go directly from natural language to executable behavior.

```text
Natural language
      ↓
Semantic IR
      ↓
Validation
      ↓
Artifact
```

### 2. Push deterministic work outside the LLM

Parsing, validation, indexing, state management and policy enforcement should be conventional code wherever possible.

### 3. Split inference by responsibility

Specialized inference passes are easier to validate, retry and observe than one giant agent-building prompt.

### 4. Treat generated agents as build artifacts

Once generated code exists, ordinary software-engineering controls should apply.

### 5. Make runtime state explicit

State machines create useful control points for retries, timeouts, verification and policy.

### 6. Assume LLM output is unreliable

Structured output, coercion, validation, confidence and post-generation checks are fundamental infrastructure.

### 7. Security follows the artifact

Once an LLM can generate executable code or tool configuration, the generated artifact becomes part of the security boundary.

---

## 18. Relevance to Akashic Records

AgentHatch maps surprisingly well onto the direction of the Akashic Intelligence Engine.

```text
Akashic note
   ↓
Deterministic parsing
   ↓
Structured note representation
   ↓
LLM semantic analysis
   ↓
Validated intermediate representation
   ↓
Derived intelligence / agents
```

Useful parallels:

- **Note model ↔ AHSSPEC** — structured representation between raw content and intelligence.
- **Knowledge grading ↔ confidence reporting** — AI-derived decisions become explicit and inspectable.
- **Knowledge graph ↔ capability/dependency graph** — relationships become first-class data.
- **Specialized agents ↔ specialized harnesses** — narrow responsibilities are easier to validate.
- **Retrieval ↔ AgentHatch KB layer** — retrieval becomes an explicit capability.
- **Agent workspace ↔ generated artifacts** — agents can have defined capabilities, inputs, outputs and provenance.

The strongest idea to borrow is **not AgentHatch itself**. It is the principle of an explicit semantic IR between unstructured knowledge and executable intelligence.

---

## 19. What I Would Borrow vs Avoid

### Borrow

- compiler-style architecture
- explicit intermediate representation
- deterministic parsing before LLM inference
- specialized inference passes
- schema/Pydantic validation
- confidence and provenance metadata
- generated artifacts
- explicit runtime state machine
- post-generation validation
- capability-oriented tool definitions
- knowledge retrieval as a first-class capability

### Avoid Copying Blindly

- treating low-temperature inference as true determinism
- assuming self-review equals correctness
- executing generated code without strong isolation
- automatically trusting inferred MCP configuration
- composing skills without explicit capability and authorization models
- making generated Python the only representation of agent behavior

---

## 20. Open Questions

- Can AHSSPEC become a stable, independently versioned agent contract?
- Can compilation become reproducible enough for meaningful artifact diffs?
- How should model/provider versions be included in provenance?
- Can generated agents be safely sandboxed at enterprise scale?
- How should tool permissions be represented in the specification?
- How should skills declare dependencies and conflicts?
- How should composition resolve capability and authorization conflicts?
- Can agents be incrementally rebuilt when only part of a skill changes?
- Can the same IR generate multiple runtime targets rather than only Python?
- Can knowledge, behavior and tools be versioned independently?
- How should stale knowledge be detected and rebuilt?
- Can the compiler support fully local/offline inference for sensitive skills?

---

## 21. Adoption Verdict

**Interesting architecture:** Yes  
**Worth experimenting with:** Yes  
**Ready to become core enterprise infrastructure:** Not yet  
**Worth borrowing architectural ideas from:** Definitely  
**Worth adopting wholesale into Akashic:** No

**Most valuable idea:** the compiler boundary and AHSSPEC-style intermediate representation.

**Biggest architectural risk:** LLM-derived executable artifacts and tool configurations crossing security boundaries.

**Biggest opportunity:** extending the compiler model from agent behavior into a governed system for compiling knowledge, capabilities, tools, policies and retrieval into agent artifacts.

---

## 22. Current Project Direction

The roadmap shows a progression roughly like:

```text
6-Harness Compilation
        ↓
Structured AHSSPEC
        ↓
Code Generation
        ↓
Post-generation Repair
        ↓
Runtime Planning
        ↓
Knowledge-backed Agents
        ↓
Skill Fusion / Meta-agent
        ↓
Marketplace / Channels
        ↓
Stronger Docker Isolation
        ↓
One-sentence → runnable agent
```

The final milestone effectively turns AgentHatch into a higher-level programming language for agents.

That direction makes the IR, provenance, testing, permissions and sandboxing layers increasingly important rather than less important.

---

## 23. Source and Evidence

Primary source reviewed:

- Repository: https://github.com/agenthatch/agenthatch
- `README.md`: architecture, CLI, pipeline and runtime
- `src/agenthatch/skill/spec.py`: AHSSPEC/AHS v1.1 models and harness contracts
- `ROADMAP.md`: implemented capabilities and planned direction
- `SECURITY.md`: security reporting and stated security process
- `agenthatch-core`: runtime and sandbox components

### Evidence model

This note uses three evidence levels:

- **Implementation evidence** — directly supported by inspected repository files.
- **Project/documentation claim** — stated by AgentHatch but not independently verified through exhaustive source inspection.
- **Architectural analysis** — interpretation or recommendation derived from the observed implementation.

The note intentionally does not treat project documentation claims as equivalent to independently verified behavior.
### Evidence boundary

Implementation files were inspected selectively rather than exhaustively. Direct repository behavior is treated as implementation evidence. Conclusions about enterprise readiness, security maturity and long-term architecture are analysis rather than claims made by the project.

**Last reviewed:** 2026-08-12
**Analysis confidence:** High