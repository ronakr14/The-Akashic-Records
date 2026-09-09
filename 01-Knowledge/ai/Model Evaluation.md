---
domain: ai
subdomain: evaluation
note_type: concept
source_type: self
status: draft
level: advanced
---
# AI Summary

DRAFT — scaffold only. Synthesis pending. Evaluating LLM systems: offline eval sets, LLM-as-judge, regression testing, and the briefings' point that production evaluation beats benchmark worship.

---

## What to evaluate

- Model vs prompt vs pipeline vs agent — different units
- Task metrics vs safety/refusal vs cost/latency

## Offline evaluation

- Building a representative eval set; golden answers vs rubrics
- Slicing by difficulty, domain, failure class
- Data leakage / contamination

## LLM-as-judge

- Rubric design, pairwise vs pointwise, position bias
- Calibrating the judge against human labels

## RAG / agent evaluation

- Retrieval metrics (recall@k, MRR) — see [[Retrieval-Augmented Generation]]
- Faithfulness / groundedness, answer relevance
- Agent: task success, steps, recovery — see [[Agent Architecture]]

## Regression testing

- Eval in CI, thresholds, flakiness from nondeterminism
- Versioning eval sets alongside prompts

## Production evaluation

- Online signals, sampling, human review queues
- Briefings theme: GitHub eval work, SWE Refactor Bench weaknesses

## Open questions

- Minimum viable eval set size for this vault's use cases?
- How to keep judge prompts stable across model upgrades?

## Reference

- [[OBLITERATUS]] — mechanistic interpretability angle
- [[_Briefings Index]] — production-evaluation-beats-benchmarks theme
- [[_AI Tools Catalog]]

## See also

- [[_AI MOC]] · [[Retrieval-Augmented Generation]] · [[Agent Architecture]] · [[Prompt Engineering]]
