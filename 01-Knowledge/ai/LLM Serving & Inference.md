---
domain: ai
subdomain: inference
note_type: concept
source_type: self
status: draft
level: advanced
---
# AI Summary

DRAFT — scaffold only. Synthesis pending. How LLM inference actually runs: batching, KV cache, quantization, the memory wall, and local vs hosted vs distributed serving.

---

## Inference basics

- Prefill vs decode; why decode is memory-bandwidth bound
- KV cache: size, growth with context, eviction
- Briefings theme: "AI inference is running into a memory wall"

## Throughput techniques

- Continuous / in-flight batching
- PagedAttention-style KV management
- Speculative decoding

## Model compression

- Quantization (int8/int4, GPTQ/AWK-style), tradeoffs
- Distillation, pruning — when each applies

## Deployment topologies

- Single-GPU local, multi-GPU tensor/pipeline parallel
- Distributed inference as a systems discipline (Ray + vLLM briefings theme)
- Hosted API vs self-host decision

## Routing & cost

- Model routers, cost-based routing (briefings: NVIDIA Switchyard)
- Caching, prompt caching — see [[Prompt Engineering]]

## Local-first angle

- On-device / commodity-hardware inference
- Fits the vault's local-first principle

## Open questions

- Break-even point: self-host vs API for this workload?
- Practical quant level before quality drops on target tasks?

## Reference

- [[Distributed Llama]] · [[CrowdLlama]] — distributed / crowd inference
- [[Hugging Face Accelerate]] — multi-device execution
- [[OGAM]] · [[Locally Uncensored]] — on-device / local desktop AI
- [[Portkey]] · [[9Router]] · [[Omniroute]] · [[BitRouter]] — LLM gateways / routing
- [[_AI Tools Catalog]]

## See also

- [[_AI MOC]] · [[Distributed System]] · [[Context Engineering]] · [[Agent Architecture]]
