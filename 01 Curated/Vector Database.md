---
domain: Data Engineering
domain_suggested: null
category: Curated
category_suggested: null
source_type: obsidian
status: review
tags: [vector-database, embeddings, similarity, rag, search]
---






```table-of-contents
```

Best use case: Semantic search and RAG pipelines — store embeddings to power similarity retrieval (docs, code, recommendations) at scale.

Alternative: [[Elasticsearch]] when you need hybrid search (BM25 + vectors) with mature filtering, aggregations, and ops tooling.

---

## Milvus — Enterprise-Grade at Scale

1. Fully open source
2. Runs locally (Docker) + distributed cloud cluster
3. Built for billions of vectors & scalability
4. Slightly heavy ops — not for prototyping

---

## Qdrant — Modern, Fast, Clean

1. Rust-based (fast + efficient)
2. Local + cloud-native
3. Excellent filtering + payload support
4. Suitable for production apps

---

## Weaviate — ML-Native Ecosystem

1. Open source
2. Local + cloud deployment
3. GraphQL + hybrid search
4. Built-in ML pipelines + APIs

---

## pgvector — Pragmatic Engineer Choice

1. Extension on PostgreSQL
2. Local + cloud (RDS, Supabase, etc.)
3. SQL + vectors together
4. Not scalable for heavy workloads

---

## Chroma — Dev-Friendly, Lightweight

1. Open source
2. Local-first
3. Cloud = DIY

---

## FAISS — Library, Not Database

1. Super fast
2. No persistence / APIs

---

## OpenSearch / Elasticsearch — Hybrid King

1. Open source
2. Local + cloud
3. Combines keyword + vector search

---

## Quick Decision Matrix

|Use Case|Pick|
|---|---|
|Just getting started|Chroma|
|Postgres ecosystem|pgvector|
|Balanced production|Qdrant|
|Massive scale / enterprise|Milvus|
|ML-heavy / GraphQL|Weaviate|
|Hybrid search|OpenSearch|

---

## See Also

- [[Elasticsearch]]
- [[Data Engineering]]
