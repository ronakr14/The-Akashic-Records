# Langchain Agents

## Core Purpose & Mental Model
- Solves: orchestrate LLM with tools, memory, reasoning.
- Mental model: Agent = LLM core + loop: think -> act -> observe -> repeat.
- Compared to raw LLM: adds planning, tool use, state.

## Best Use Cases & Capabilities
- Shines when need multi-step reasoning, external data, APIs.
- Examples: data pipeline validation, dynamic SQL generation, research assistant, personal knowledge management.
- Good at: chat with tools, autonomous task execution, conditional workflows.

## Where NOT to Use It
- Simple QA: overhead.
- High throughput low latency: extra layers.
- Deterministic workflows: better with pure code.
- Anti-pattern: using agent for static prompt chaining; use LCEL instead.

## Alternatives
- Semantic Kernel (MS): similar, tighter .NET integration, less community.
- LlamaIndex Agents: focus on data indexing, lighter.
- AutoGPT: early, less reliable.
- CrewAI: role-based, higher abstraction.
- Commercial: Azure AI Studio, AWS Bedrock Agents.
Compare: performance similar; flexibility: Langchain high; ease: Langchain moderate due to many moving parts.
- Why choose: need broad tool ecosystem, JavaScript/Python support.

## Efficient Usage Strategies
- Reuse LLM instance, limit tool calls.
- Cache intermediate results.
- Avoid recursive agent spawning.
- Use structured output (JSON) to reduce parsing.
- Experienced tip: set max iterations, use fallback to direct LLM.

## If Had to Build From Scratch
- Core: LLM wrapper, prompt template, parser.
- Loop: while not done: generate action, execute, update state.
- Needs: planning algorithm (ReAct, Plan-and-Execute), tool registry, memory store.
- Learn: prompt engineering, finite state machines, async queues.

## Tradeoffs & Limitations
- Breaks at scale: latency accumulates, cost per token.
- Bottleneck: LLM call frequency.
- Hidden: prompt drift, tool failure handling.
- Operational: debugging non-deterministic paths, monitoring.

## Ecosystem & Maturity
- Ecosystem: large, many integrations (vector stores, APIs).
- Community: active, frequent updates.
- Tooling: LangSmith for tracing.
- Talent: growing, but expertise varies.

## Bottom Line
Choose when need flexible reasoning with tools; else use simpler chain or direct LLM.
One-line: If agent loop adds value over static chain, use Langchain Agents.