# AI Agents

## Core Purpose & Mental Model
Problem: automate complex goal-directed tasks needing reasoning, tool use, memory.
Mental model: LLM core + loop think->act->observe until goal met.
Vs others: unlike pure chains, agents keep state, decide next steps autonomous.

## Best Use Cases & Capabilities
Shines: multi-step data pipelines needing adaptive decisions, LLM research assistants, dynamic workflow orchestration, PKM with context retrieval.
Examples:
- Data eng: agent monitors data quality, triggers reruns, updates metadata on anomalies.
- LLM systems: agent self-corrects prompts, fetches external docs, iterates answers.
- AI systems: agent coordinates models, handles fallback, load balancing.
- Agentic AI: hierarchical agents manager delegates specialists.
- PKM: agent tags notes, suggests links, builds knowledge graphs from text.

## Where NOT to Use It
Poor: simple deterministic tasks (fixed-schema ETL), low-latency real-time, high-frequency trading.
Anti-patterns: agents for static DAGs, over-engineered chatbots with agent loops.
Better: plain scripts, workflow engines (Airflow, Prefect), rule-based.

## Alternatives (Open Source & Paid)
LangGraph: graph-based agent framework. Performance moderate, scalability good async, flexibility high, ease medium.
LlamaIndex Agent: retrieval-augmented agents. Performance good RAG, scalability index-dependent, flexibility medium, ease high.
AutoGen: multi-agent conversation. Performance okay, scalability suffers many agents, flexibility high, ease medium.
CrewAI: role-based teams. Performance similar LangGraph, scalability moderate, flexibility high, ease high.
OpenAI Assistants API: managed. Performance good, scalability handled OpenAI, flexibility limited tools, ease high.
Choose: LangGraph custom control, LlamaIndex RAG-heavy, AutoGen conversational multi-agent, CrewAI role play, Assistants quick managed.

## Efficient Usage Strategies
Practices: limit tool calls per loop, cache results, structured outputs, timeout, max iter.
Cost opt: smaller LLM planner, larger only generation, batch requests, embedding caches.
Mistakes: infinite loops, overloading context, no tool failure handling.
Tips: human-in-loop approvals, token-efficient prompt compress, persist state extern.

## If I Had to Build This From Scratch
Components: LLM interface, planner prompt, memory short/long term, tool executor, scheduler loop.
Learn: prompt engineering, finite state machines, dependency injection, event loops.
Algos: tree-of-thoughts, reflexion, ReAct, ADPL.
Structs: stack call stack, hash map memory, queue tool results.
Design: stateless worker, Redis memory, async IO tool calls.

## Tradeoffs & Limitations
Breaks scale: LLM latency bottleneck, token cost loops, hallucination planning.
Hidden: tool desc length prompt size, concurrent tool calls complexity.
Ops: debug non-deterministic loops, monitor trajectories, ensure safety.

## Ecosystem & Maturity
Ecosystem: fast growing, many frameworks, standards lacking.
Community: active GitHub, Discord; tooling improving LangSmith, Arize.
Hiring: talent scarce, premium agents exp.

## Bottom Line
Choose agents when task needs adaptive reasoning, tool use; else simpler orch.
Framework: steps depend dynamic outcomes -> agent; else -> DAG.

# AI Agents

Best use case:  
Automate multi-step workflows by letting LLMs plan, call tools, and iterate (e.g., research, ops automation, end-to-end task execution).

Alternative: — **Rule-based automation (e.g., Airflow)** (better for deterministic, auditable workflows with strict reliability needs)
