---
domain: ai
subdomain: rag
note_type: concept
source_type: self
status: draft
level: intermediate
---
# AI Summary

DRAFT — scaffold only. Synthesis pending. RAG: grounding an LLM's answer in retrieved documents instead of parametric memory — the pipeline (chunk → embed → index → retrieve → rerank → assemble context → generate) and where each stage fails.

---

## Why RAG

- What problem it solves vs fine-tuning vs long context
- When RAG is the wrong tool

## Pipeline stages

### Chunking
- Fixed-size vs semantic vs structural (headings, code blocks)
- Chunk size / overlap tradeoffs
- Metadata carried per chunk

### Embedding
- Model choice, dimensionality, domain fit
- See [[Vector Database]] for the index layer

### Retrieval
- Dense vs sparse (BM25) vs hybrid
- Top-k, MMR, diversity

### Reranking
- Cross-encoder rerank after cheap first-stage retrieval
- Cost vs quality

### Context assembly
- Ordering, deduplication, citation, token budget
- Connects to [[Context Engineering]]

## Evaluation

- Retrieval metrics (recall@k, MRR) vs answer metrics (faithfulness, relevance)
- See [[Model Evaluation]]

## Failure modes

- Retrieval miss, distractor passages, lost-in-the-middle, stale index, chunk boundary cuts context

## Open questions

- Chunking strategy for mixed prose + code + tables?
- When does hybrid retrieval actually beat dense alone here?
- Incremental re-indexing cadence?

## Reference

- [[Onyx]] — enterprise RAG system, end-to-end
- [[Claude Context]] — code-specific retrieval
- [[FAISS (Facebook AI Similarity Search)]] · [[Turbovec]] — vector indexes
- [[BigSet]] — retrieval-adjacent dataset building
- [[_AI Tools Catalog]]

## See also

- [[_AI MOC]] · [[Vector Database]] · [[Context Engineering]] · [[Model Evaluation]]
