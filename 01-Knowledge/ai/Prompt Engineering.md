---
domain: ai
subdomain: prompting
note_type: concept
source_type: self
status: draft
level: intermediate
---
# AI Summary

DRAFT — scaffold only. Synthesis pending. Practical patterns for getting reliable output from an LLM: instruction structure, examples, structured output, decomposition — and where prompt work stops and [[Context Engineering]] takes over.

---

## Instruction structure

- Role, task, constraints, output format, refusal conditions
- Ordering effects; putting the ask last
- Cross-ref [[LLM Interaction Guide]] (decision-mode vs exploration-mode)

## Examples

- Zero-shot vs few-shot; when few-shot hurts
- Example selection, ordering, format consistency

## Structured output

- JSON / schema-constrained decoding, tool-call formatting
- Validation + repair loop

## Decomposition

- Chain-of-thought, step lists, self-critique / reflection
- Splitting one hard prompt into a pipeline

## Robustness

- Prompt injection, delimiter discipline, untrusted content handling
- Determinism: temperature, seeds, caching

## Where prompting ends

- When the fix is retrieval, context budget, or fine-tuning, not wording
- See [[Context Engineering]], [[Retrieval-Augmented Generation]]

## Open questions

- How much does prompt phrasing still matter on current frontier models?
- Reusable prompt-pack structure for this vault — see `08-Prompts/`

## Reference

- [[OpenSpec]] · [[PAUL]] — spec-driven / AI-assisted development prompting
- [[Token Optimizer MCP]] — prompt/context token reduction
- [[_AI Tools Catalog]]

## See also

- [[_AI MOC]] · [[LLM Interaction Guide]] · [[Context Engineering]] · [[Model Evaluation]]
