---
domain: ai
subdomain: index
note_type: moc
source_type: self
status: curated
level: intermediate
---
# AI Summary

Map of content for the AI knowledge area. Indexes the synthesized AI notes and links to the repo-by-repo tool catalog in `06-Reference/ai/`. The core-concept notes are currently `draft` scaffolds — structure and links in place, synthesis pending.

---

# AI — Map of Content

Entry point for the AI knowledge area.

## Working with LLMs

- [[LLM Interaction Guide]] — structuring AI conversations around decisions, not information gathering: exploration vs decision mode, constraints-first, tradeoffs over features, adversarial critique, lightweight ADRs

## Adjacent knowledge

- [[Vector Database]] — embedding storage, ANN indexes, similarity search (filed under database)

## Projects

- [[Distributed LLM]] — home-lab distributed inference across laptops (llama.cpp RPC); hands-on backing for [[LLM Serving & Inference]]

## Reference

- [[_AI Tools Catalog]] — 50+ open-source AI projects analysed repo-by-repo (gateways, agent frameworks, RAG, inference, security). Lookup-tier, not synthesized.

## Core concepts (draft scaffolds)

Structure + cross-links in place; needs synthesis from experience.

- [[Retrieval-Augmented Generation]] — chunk → embed → retrieve → rerank → assemble → generate, and where each stage fails
- [[Agent Architecture]] — control loop, tools, memory, planning, multi-agent, harness vs model
- [[Prompt Engineering]] — instruction structure, examples, structured output, decomposition, robustness
- [[Model Evaluation]] — offline eval sets, LLM-as-judge, regression testing, production eval
- [[LLM Serving & Inference]] — batching, KV cache, quantization, the memory wall, local vs hosted
- [[Context Engineering]] — window budgeting, compaction, governed/semantic context

## Remaining gaps

- Embeddings — model choice, dimensionality, domain adaptation (currently folded into [[Vector Database]] + [[Retrieval-Augmented Generation]])
- Fine-tuning vs RAG vs long-context decision guide

## See also

- [[_Data Engineering MOC]] — pipelines and storage that feed AI systems
- [[_Software Engineering MOC]] — service architecture for AI platforms
