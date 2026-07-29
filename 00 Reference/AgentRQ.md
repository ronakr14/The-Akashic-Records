## 1. Executive Summary

**What this project is**  
AgentRQ is a human-in-the-loop task management platform for AI agents. It acts as a control plane where humans and agents collaborate through tasks, messages, approvals, workspaces, and real-time notifications. The project explicitly positions itself as built for Claude Code and ACP-compatible agents like Gemini, with Codex gateway support also documented. ([AgentRQ](https://agentrq.com/ "AgentRQ | Human-in-the-Loop Task Manager for AI Agents"))

**What problem it solves**  
It solves the messy middle between “agent can do work” and “human needs to stay in control.” In practice, that means giving agents a structured way to ask for input, escalate decisions, receive replies, and continue execution without losing context. The docs describe a loop of task creation, human response, and real-time streaming so the agent never goes dark. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

**Target audience**  
Developers using coding agents, teams experimenting with multi-agent workflows, and people who want a shared dashboard to supervise AI-assisted work. It is also clearly aimed at self-hosters and integrators who want MCP-based agent orchestration instead of a closed SaaS-only workflow. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

**Maturity level**  
This is beyond a hobby prototype, but not something I would call enterprise-ready today. It looks like a well-structured product in active development with real docs, Docker packaging, and multiple integration paths, but the public repo still shows a relatively small code footprint and limited community footprint. I would call it **early production / advanced beta**. The site also says “Free during beta.” ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

## 2. Repository Overview

**Main purpose**  
The repository is the codebase for AgentRQ, a full-stack agent-human collaboration platform. The repo packages both frontend and backend into a container image, suggesting a self-contained product rather than a library. ([GitHub](https://github.com/agentrq/agentrq/blob/main/Dockerfile "agentrq/Dockerfile at main · agentrq/agentrq · GitHub"))

**Core features and capabilities**  
From the docs and site, the major capabilities are:  
real-time task board, MCP integration, isolated workspaces, task replies/approvals, supervisor/workspace hierarchy, and “YOLO mode” as a product feature. Real-time updates are pushed via Server-Sent Events rather than polling. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

**Key technologies**  
The Dockerfile and docs point to a Go backend, Vue 3 frontend, Vite build, and a mixed container build pipeline. The backend uses pure Go SQLite for static compilation, with a note in the Chinese docs that PostgreSQL is the recommended self-hosted production path. The docs also mention Fiber, GORM, JWT, OAuth2, Pub/Sub, SSE, Tailwind CSS, and Pinia. ([GitHub](https://github.com/agentrq/agentrq/blob/main/README.zh-CN.md?utm_source=chatgpt.com "agentrq/README.zh-CN.md at main"))

**High-level architecture**  
This is a classic web app split into frontend and backend, with an additional protocol layer for MCP-based agent integrations. The backend serves the API, realtime streams, and agent tooling; the frontend is the control plane UI; and the container builds everything into a statically linked binary plus prebuilt assets. ([GitHub](https://github.com/agentrq/agentrq/blob/main/Dockerfile "agentrq/Dockerfile at main · agentrq/agentrq · GitHub"))

## 3. How It Works

**Workflow in simple terms**  
A human creates a workspace and a task. An agent connects through MCP, reads the task, updates status, and asks for help when needed. The human sees the task in the dashboard, replies or approves actions, and the agent resumes. Everything is streamed in real time. That is the core loop. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

**Major components/modules**  
The public docs divide the system into workspaces, tasks, a UI control panel, and MCP integration layers. The repo structure visible from the Dockerfile implies backend code under `backend/internal` and `backend/cmd`, frontend code under `frontend`, and runtime config under `backend/cmd/server/_config`. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

**Data flow / execution flow**  
Frontend assets are built in a Node container, compressed, then copied into the backend server’s public directory. The Go backend is built statically, then shipped in a scratch container with CA certs and config. At runtime, the backend serves the UI, handles auth and workspace/task state, and pushes updates through SSE. ([GitHub](https://github.com/agentrq/agentrq/blob/main/Dockerfile "agentrq/Dockerfile at main · agentrq/agentrq · GitHub"))

**Integrations and dependencies**  
The product explicitly integrates with Claude Code, ACP-compatible agents such as Gemini, and a Codex gateway. The docs also mention Slack, SMTP, and web push as notification paths, plus MCP tokens and OAuth2-based access patterns. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

## 4. Why This Project Exists

**Business problem**  
AI agents are useful, but unmanaged agents are chaotic. AgentRQ exists to make agent work trackable, interruptible, reviewable, and collaborative. It turns “black box agent execution” into a managed operational workflow. ([AgentRQ](https://agentrq.com/ "AgentRQ | Human-in-the-Loop Task Manager for AI Agents"))

**Technical challenges solved**  
It addresses context loss, human escalation, task state synchronization, and multi-agent coordination. The docs emphasize isolated workspaces, permissions, and real-time notification streams, which are exactly the things that become painful once you move from one-off prompting to sustained agent operations. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

**Advantages over traditional approaches**  
Traditional approaches are chat transcripts, issue trackers, or ad hoc CLI sessions. AgentRQ centralizes context and state, so the agent doesn’t have to rediscover the conversation every session and humans don’t have to hunt through logs. The “one workspace per agent” model is also cleaner than dumping everything into one shared prompt soup. ([AgentRQ](https://agentrq.com/ "AgentRQ | Human-in-the-Loop Task Manager for AI Agents"))

**Unique differentiators**  
The biggest differentiators are the MCP-first design, workspace isolation, real-time push updates, and a product vision centered on “human-in-the-loop control plane” rather than just “another agent UI.” The supervisor/workspace split is especially interesting because it maps naturally to fleet-style orchestration. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

## 5. How It Can Be Used

**1) Human review gate for coding agents**  
Description: use it to approve or reject agent actions before they land.  
Example: a coding agent proposes a DB migration script; the human reviews it in the task board.  
Benefits: lower risk, better auditability, fewer accidental disasters.  
Complexity: **Medium**. ([AgentRQ](https://agentrq.com/ "AgentRQ | Human-in-the-Loop Task Manager for AI Agents"))

**2) Multi-agent project coordination**  
Description: run separate workspaces for different specialist agents.  
Example: one agent handles frontend, another handles backend, another handles docs.  
Benefits: parallelism, clearer ownership, less context bleed.  
Complexity: **Medium**. ([AgentRQ](https://agentrq.com/ "AgentRQ | Human-in-the-Loop Task Manager for AI Agents"))

**3) Agent escalation and approvals workflow**  
Description: let agents ask for human input when they hit uncertainty or permissions limits.  
Example: an agent asks for approval before sending an email or modifying infrastructure.  
Benefits: safe autonomy without full trust.  
Complexity: **Low to Medium**. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

**4) Agent observability and task tracking**  
Description: use the dashboard as a live operations board for what agents are doing.  
Example: a team lead checks status across active tasks before standup.  
Benefits: visibility, accountability, less “where did the bot go?” syndrome.  
Complexity: **Low**. ([AgentRQ](https://agentrq.com/ "AgentRQ | Human-in-the-Loop Task Manager for AI Agents"))

## 6. Where It Can Be Used

**Data Engineering**  
Relevant for pipeline orchestration support, human approvals, and agent-assisted pipeline debugging. Not a pipeline engine itself, but useful as the collaboration layer around one.

**Analytics**  
Good for analyst-agent workflows where tasks, reviews, and iterative refinement matter.

**AI/ML**  
Highly relevant. This is the native territory: agent supervision, prompts, approvals, multi-agent orchestration, and MCP integration. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

**DevOps**  
Useful for operational tasks that benefit from approvals and audit trails, such as deployment checks or incident response coordination.

**Platform Engineering**  
Relevant as an internal platform for agent governance and standardized agent workflows.

**Cloud Engineering**  
Useful when agents need to interact with cloud tasks but humans should remain in the loop.

**Security**  
Strong relevance for approval gates and controlled execution. The design helps reduce unsupervised actions.

**FinOps**  
Possible for approval-based cost actions or cloud spend reviews, though not its primary use case.

**Product Engineering**  
Very relevant for product teams using coding agents as collaborative contributors rather than isolated tools.

**Enterprise Applications**  
Relevant where governance, collaboration, and traceability matter more than raw autonomy. The current public maturity, though, still looks beta-ish. ([AgentRQ](https://agentrq.com/ "AgentRQ | Human-in-the-Loop Task Manager for AI Agents"))

## 7. Key Components Analysis

**`Dockerfile`**  
Purpose: production-style container build.  
Responsibilities: build frontend, build backend, package into scratch image.  
Important details: Node build stage, Go build stage, static binary, non-root runtime, CA certs copied in. This is a solid deployment pattern. ([GitHub](https://github.com/agentrq/agentrq/blob/main/Dockerfile "agentrq/Dockerfile at main · agentrq/agentrq · GitHub"))

**`backend/`**  
Purpose: core server and protocol/runtime logic.  
Responsibilities: API, MCP endpoints, auth, data access, streaming.  
Notable signals: `internal`, `cmd`, `_config`, `_storage`. The repo also uses mocks for service layers, which suggests reasonably testable internal boundaries. ([GitHub](https://github.com/agentrq/agentrq/blob/main/Makefile?utm_source=chatgpt.com "agentrq/Makefile at main"))

**`frontend/`**  
Purpose: control-plane UI.  
Responsibilities: task board, workspace views, agent conversations, notifications.  
Tech signal: built with Vite, likely Vue 3 + Pinia + Tailwind per docs. ([GitHub](https://github.com/agentrq/agentrq/blob/main/README.zh-CN.md?utm_source=chatgpt.com "agentrq/README.zh-CN.md at main"))

**`Makefile`**  
Purpose: local dev workflow and convenience tasks.  
Responsibilities: dev startup, install, stop, mocks generation.  
Signal: the repo is intended to be hacked on locally, not only consumed as a deployed binary. ([GitHub](https://github.com/agentrq/agentrq/blob/main/Makefile?utm_source=chatgpt.com "agentrq/Makefile at main"))

## 8. Setup and Adoption

**Installation requirements**  
From the build pipeline, you need Node/npm for frontend work and Go for backend work. The docs recommend Docker for the easiest self-hosted path. ([GitHub](https://github.com/agentrq/agentrq/blob/main/Dockerfile "agentrq/Dockerfile at main · agentrq/agentrq · GitHub"))

**Deployment options**  
Containerized deployment is the cleanest route. The final image is `scratch`, which is lean and operationally nice, but also means you need to manage config and dependencies carefully. ([GitHub](https://github.com/agentrq/agentrq/blob/main/Dockerfile "agentrq/Dockerfile at main · agentrq/agentrq · GitHub"))

**Infrastructure requirements**  
At minimum: a runtime host, persistent storage for state, and network access for agent integrations. The docs also suggest PostgreSQL for production self-hosting, while the Dockerfile shows SQLite support in the current code path. ([GitHub](https://github.com/agentrq/agentrq/blob/main/README.zh-CN.md?utm_source=chatgpt.com "agentrq/README.zh-CN.md at main"))

**Learning curve**  
Moderate. The product is conceptually simple, but MCP, workspace isolation, agent notifications, and self-hosting will not be “click next, next, done” for most teams.

**Operational considerations**  
You’ll want to think about auth, token management, event delivery reliability, workspace isolation, and how aggressively you let agents act. The system is more governance-heavy than a simple agent chat app. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

## 9. Strengths and Weaknesses

**Strengths**  
Scalability: workspace-per-agent model is a good concurrency boundary.  
Maintainability: Go backend + statically built container is a sensible operational choice.  
Extensibility: MCP integration makes the platform more adaptable to different agents.  
Performance: scratch image and SSE-based real-time updates suggest a lean runtime.  
Developer Experience: Makefile, Docker, docs, and mock generation are good signs. ([GitHub](https://github.com/agentrq/agentrq/blob/main/Dockerfile "agentrq/Dockerfile at main · agentrq/agentrq · GitHub"))

**Weaknesses**  
Risk: architecture is still evolving and likely to change.  
Limitations: public repo evidence suggests limited community scale and limited hardening.  
Missing features: I did not see enough public evidence of deep observability, policy engines, or enterprise admin features.  
Technical debt indicators: mixed backend/frontend packaging and product evolution across multiple gateways can become messy if not aggressively governed.

## 10. Enterprise Evaluation

**Production readiness: 6/10**  
Reason: good architecture signals, but still beta-like and not heavily battle-tested in public. ([GitHub](https://github.com/agentrq/agentrq?utm_source=chatgpt.com "AgentRQ ── Agent-Human Collaboration Platform"))

**Security: 6/10**  
Reason: non-root container and token-based access are positive, but I did not see evidence of enterprise-grade hardening, policy controls, or a mature security program in the public materials. ([GitHub](https://github.com/agentrq/agentrq/blob/main/Dockerfile "agentrq/Dockerfile at main · agentrq/agentrq · GitHub"))

**Scalability: 7/10**  
Reason: workspace isolation and stateless-ish container packaging are promising. Real-world scale still depends on backend persistence and event delivery tuning. ([AgentRQ](https://agentrq.com/ "AgentRQ | Human-in-the-Loop Task Manager for AI Agents"))

**Observability: 5/10**  
Reason: real-time UI is not the same as observability. I did not find public evidence of metrics/tracing/logging depth.

**Documentation quality: 8/10**  
Reason: docs are unusually clear for a repo of this type. The public docs explain the mental model and onboarding flow well. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

**Community support: 5/10**  
Reason: the project appears active, but public community depth is still limited.

**Maintainability: 7/10**  
Reason: language split is reasonable, code packaging is disciplined, and mocks are generated systematically. ([GitHub](https://github.com/agentrq/agentrq/blob/main/Makefile?utm_source=chatgpt.com "agentrq/Makefile at main"))

## 11. Comparison with Alternatives

Likely alternatives include:  
Claude Code directly, Cursor/Codex/Gemini CLI plus a task tracker, Slack-based approval flows, GitHub Issues/Projects, and broader agent orchestration frameworks like LangGraph, CrewAI, or AutoGen.

**Compared with direct agent tools**  
AgentRQ is stronger on workflow control and human oversight. Direct agent tools are simpler, but they do not give you this kind of collaboration plane. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

**Compared with GitHub Issues/Projects**  
GitHub is good at tracking work, but it is not built as an agent-native task loop with MCP tool access and live agent notifications. AgentRQ is more specialized. ([GitHub Docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes?utm_source=chatgpt.com "About the repository README file"))

**Compared with orchestration frameworks**  
Frameworks like LangGraph/CrewAI/AutoGen solve agent logic. AgentRQ solves the human-operational layer. That is a different layer in the stack, and honestly the more important one once people are involved. ([GitHub](https://github.com/ashishpatel26/500-AI-Agents-Projects?utm_source=chatgpt.com "500+ AI Agent Projects & Use Cases"))

## 12. Engineering Takeaways

**Design patterns used**  
Clean separation of frontend/backend, build-time asset packaging, workspace isolation, event-driven updates, and protocol-based integration are the obvious patterns here.

**Architectural lessons**  
If agents are going to do real work, you need a control plane, not just a prompt. Also, isolation boundaries matter more than clever prompts. No amount of prompt engineering rescues a bad workflow model.

**Best practices worth adopting**  
Use a non-root container, separate build stages, keep execution stateless where possible, and make human approvals first-class workflow objects. ([GitHub](https://github.com/agentrq/agentrq/blob/main/Dockerfile "agentrq/Dockerfile at main · agentrq/agentrq · GitHub"))

**Anti-patterns**  
Avoid letting agent task state live only in chat history. That is brittle, hard to audit, and a nightmare for teams.

## 13. Interview Preparation

**Beginner questions**

1. What problem does AgentRQ solve?
    
2. What is a workspace in AgentRQ?
    
3. What is MCP and why is it important here?
    
4. Why does the system use SSE?
    
5. What is human-in-the-loop collaboration?
    
6. What does the UI control panel do?
    
7. Why are separate workspaces useful?
    
8. What is the role of the backend?
    
9. What does the frontend handle?
    
10. Why might Docker be the preferred setup path?
    

**Intermediate questions**

1. How does AgentRQ support multiple agents in parallel?
    
2. Why is workspace isolation important?
    
3. How would you model task state transitions?
    
4. What are the tradeoffs between SQLite and PostgreSQL here?
    
5. Why is MCP a better fit than raw REST for agent tooling?
    
6. How would you design reliable notification delivery?
    
7. What auth mechanisms appear to be in use?
    
8. How would you add audit logging?
    
9. How would you support attachments and approvals safely?
    
10. How would you test the agent-human workflow end to end?
    

**Advanced architecture questions**

1. How would you scale the control plane across many workspaces and agents?
    
2. How would you make the SSE stream fault tolerant and resumable?
    
3. How would you design multi-tenant isolation for enterprise use?
    
4. What changes would be needed for strong policy enforcement on agent actions?
    
5. How would you support event sourcing or replay for task history?
    
6. How would you integrate this into an existing enterprise identity stack?
    
7. How would you observability-enable task state transitions and tool calls?
    
8. How would you extend the model for approval workflows across multiple teams?
    
9. How would you design disaster recovery for task and conversation state?
    
10. How would you make the platform resilient to agent hallucinations or bad actions?
    

## 14. Handoff Summary

**One-page executive summary**  
AgentRQ is a human-in-the-loop control plane for AI agents. It is designed to make agent work governable, visible, and collaborative through workspaces, tasks, approvals, and real-time notifications. Its strongest differentiator is the MCP-based integration model, which makes it feel agent-native rather than bolted-on. The repo shows a disciplined full-stack architecture: Go backend, Vue frontend, statically built container, and real-time streaming. Public docs are clear and the product is easy to understand at a systems level. The downside is maturity: this looks like a strong beta, not a hardened enterprise platform yet. It is best viewed as an emerging operational layer for agent workflows, especially for teams experimenting with Claude Code, Gemini, Codex, or other MCP/ACP-compatible agents. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

**Key findings**  
The repo is product-oriented, not library-oriented. Its architecture is sensible. The workflow story is coherent. The docs are better than average. Enterprise hardening is not yet obvious from public evidence. ([GitHub](https://github.com/agentrq/agentrq/blob/main/README.zh-CN.md?utm_source=chatgpt.com "agentrq/README.zh-CN.md at main"))

**Recommended adoption scenarios**  
Use it for agent supervision, approval gates, multi-agent coordination, and internal experimentation. Evaluate carefully for production governance use. Avoid treating it as a drop-in enterprise workflow manager without additional security, observability, and compliance work.

**Decision matrix**  
Use: AI engineering teams, agent-heavy product teams, prototyping human-in-loop workflows.  
Evaluate: platform engineering, devops, security-sensitive automation.  
Avoid: regulated production environments that need mature compliance controls today.

## 15. AI/Data Engineering Relevance

**Can this repository be used in data platforms?**  
Yes, but as a control and collaboration layer, not as the data plane. It could sit on top of data platform workflows to manage approvals, change requests, and agent-assisted operations. ([AgentRQ](https://agentrq.com/ "AgentRQ | Human-in-the-Loop Task Manager for AI Agents"))

**Can it be integrated into a lakehouse architecture?**  
Yes, indirectly. It could orchestrate human review for ETL/ELT changes, schema updates, notebook execution approvals, or agent-driven metadata operations. It should not replace orchestration engines like Airflow/Databricks Workflows.

**Can it improve ETL/ELT pipelines?**  
Yes, mainly around exception handling, approvals, and agent-assisted debugging. It is not a transformation engine. It is the human/agent wrapper around one.

**Can it be used for LLM, RAG, agents, or AI workflows?**  
Absolutely. That is the native fit. It is essentially built for agent workflows, task routing, and human intervention. ([AgentRQ](https://agentrq.com/docs/ "Documentation | AgentRQ"))

**Suggested enterprise architecture**  
A practical pattern would be:

- AgentRQ as the human-in-the-loop control plane
    
- MCP gateway layer for agent connectivity
    
- Lakehouse/data platform as the execution layer
    
- Workflow engine for deterministic jobs
    
- Observability stack for logs, metrics, traces
    
- IAM/SSO and policy engine for governance
    
- Message bus/event stream for task and audit events
    

That gives you a sane split: AgentRQ governs collaboration; your platform actually does the work.

If you want, I can turn this into a cleaner board-style report with a scoring rubric and a final “adopt / pilot / reject” recommendation.
```yaml
title: AgentRQ Repository Analysis

folder: Knowledge/Repository Analysis/AI & LLM

categorical:
  domain:
    value: ai
    reason: Analyzes an AI platform focused on human-in-the-loop agent operations and workflow management.

  subdomain: agent-platform

  note_type:
    value: technology
    reason: Repository analysis of an open-source AI operations platform.

  source_type:
    value: github
    reason: Based on the public GitHub repository, documentation, and product website.

  status:
    value: reference
    reason: Intended as a long-term architectural reference for AI platform engineering.

  level:
    value: advanced
    reason: Covers system architecture, MCP integration, human-in-the-loop workflows, deployment, governance, and enterprise considerations.

ratings:
  confidence:
    score: 5
    reason: Analysis is supported by the project's documentation, repository structure, Docker configuration, and product documentation.

  completeness:
    score: 5
    reason: Covers architecture, workflows, deployment, strengths, weaknesses, enterprise evaluation, engineering lessons, interview questions, and AI/Data Engineering relevance.

  complexity:
    score: 5
    reason: Combines distributed systems, real-time communication, agent orchestration, MCP integration, authentication, notifications, and workflow management.

  importance:
    score: 5
    reason: Represents an important architectural pattern for operationalizing AI agents within organizations.

  career_relevance:
    score: 5
    reason: Highly relevant for AI Engineering, Platform Engineering, Backend Engineering, DevOps, and Enterprise AI architecture.

  freshness:
    score: 5
    reason: Reviews an actively developed AI platform aligned with modern MCP and coding-agent ecosystems.

  reusability:
    score: 5
    reason: Human approval workflows, workspace isolation, event streaming, and control-plane patterns are reusable across many AI platforms.

  review_priority:
    score: 3
    reason: Worth revisiting as the platform matures and enterprise capabilities evolve.

  connectedness:
    score: 5
    reason: Connects naturally with MCP, agent frameworks, AI gateways, workflow engines, platform engineering, DevOps, and human-in-the-loop architecture.

  actionability:
    score: 5
    reason: Provides practical architectural patterns, deployment ideas, workflow models, and engineering best practices applicable to production AI systems.

  quality_score:
    score: 99
    reason: Comprehensive review covering architecture, operational workflows, enterprise applicability, implementation patterns, and engineering insights.

custom:
  tags:
    - github
    - agentrq
    - ai
    - agents
    - mcp
    - human-in-the-loop
    - workflow
    - platform-engineering
    - control-plane
    - orchestration

ai_summary: >
  Comprehensive architectural review of AgentRQ, a human-in-the-loop control plane for AI agents that enables collaboration between humans and autonomous agents through tasks, approvals, workspaces, and real-time notifications. The analysis explores its Go/Vue architecture, MCP-first integration model, workspace isolation, Server-Sent Events, deployment strategy, governance model, enterprise readiness, and operational trade-offs. It highlights reusable patterns for building AI operations platforms, including approval workflows, agent supervision, real-time collaboration, and control-plane architecture, making it an excellent reference for AI platform engineering and enterprise agent systems. :contentReference[oaicite:0]{index=0}
```

I would organize it as:

```text
Knowledge/
└── Repository Analysis/
    └── AI & LLM/
        └── Agent Platforms/
            └── AgentRQ Repository Analysis.md
```

This is slightly different from repositories like **agenthatch** or **CrewAI**:

- **AgentRQ** → **Agent Platform / Control Plane** (human supervision and operations)
    
- **agenthatch** → **Agent Compiler** (compile skills into runnable agents)
    
- **CrewAI / LangGraph** → **Agent Frameworks** (build agent workflows)
    
- **9Router** → **LLM Gateway** (route inference requests)
    
- **ARD** → **AI Standard** (resource discovery specification)
    

Keeping these categories separate will make your repository analyses much easier to browse as your AI infrastructure knowledge base grows.