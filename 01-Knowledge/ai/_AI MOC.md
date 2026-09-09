---
domain: ai
subdomain: index
note_type: moc
source_type: self
status: curated
level: intermediate
---
# AI Summary

Map of content for the AI knowledge area. Indexes the synthesized AI notes and links to the repo-by-repo tool catalog in `06-Reference/ai/`. This domain is currently thin — most AI material is still reference-tier — so the gap list below is the working agenda for what to synthesize next.

---

# AI — Map of Content

Entry point for the AI knowledge area.

## Working with LLMs

- [[LLM Interaction Guide]] — structuring AI conversations around decisions, not information gathering: exploration vs decision mode, constraints-first, tradeoffs over features, adversarial critique, lightweight ADRs

## Adjacent knowledge

- [[Vector Database]] — embedding storage, ANN indexes, similarity search (filed under database)

## Reference

- [[_AI Tools Catalog]] — 50+ open-source AI projects analysed repo-by-repo (gateways, agent frameworks, RAG, inference, security). Lookup-tier, not synthesized.

## Gaps — to develop

Topics with no synthesized note yet. Promote from reference or write from experience.

- Retrieval-augmented generation — chunking, embeddings, reranking, eval (see [[Vector Database]] for the storage layer)
- Agent architecture — planning loops, tool use, memory, multi-agent
- Prompt engineering — patterns, structured output, few-shot vs zero-shot
- Model evaluation — offline eval, LLM-as-judge, regression testing
- LLM serving & inference — batching, quantization, KV cache, local vs hosted
- Context engineering — window management, compaction, retrieval budgeting

## See also

- [[_Data Engineering MOC]] — pipelines and storage that feed AI systems
- [[_Software Engineering MOC]] — service architecture for AI platforms
