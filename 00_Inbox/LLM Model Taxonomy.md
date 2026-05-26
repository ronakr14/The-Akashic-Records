# LLM Model Taxonomy

## Summary
Reference taxonomy for LLM model types and families. Covers architecture categories, size/efficiency variants, multimodal models, reasoning-oriented models, and action-oriented models.

## Tags
#type/reference #concept/llm #status/done

---

## Core Architecture

| Type | Description |
|------|-------------|
| **LLM** | Baseline: text-in → text-out, trained on massive corpora |
| **GPT** | Decoder-only transformer optimized for generation. Strong at chat, coding, reasoning |
| **MLM** | BERT-style. Predict missing tokens. Good for understanding (search, classification), not generation |

---

## Size / Efficiency Variants

| Type | Description |
|------|-------------|
| **SLM** | Compressed LLM (few billion params or less). Fast, cheap, local. Trade-off: weaker reasoning |
| **MoE** | Mixture of Experts. Many sub-models, only a few activated per query. Scales performance without proportional compute |

---

## Multimodal / Sensory

| Type | Description |
|------|-------------|
| **VLM** | Vision-Language Model. Handles images + text. Use: OCR, visual Q&A, UI automation |
| **SAM** | Segment Anything Model. Computer vision for object segmentation. Not a language model |

---

## Reasoning-Oriented

| Type | Description |
|------|-------------|
| **LRM** | Large Reasoning Model. Tuned for multi-step reasoning (math, logic, planning). Better chain-of-thought |
| **HRM** | Hierarchical Reasoning Model. Breaks problems into sub-tasks across levels (planner → executor → verifier) |

---

## Action + Agent-Oriented

| Type | Description |
|------|-------------|
| **LAM** | Language Action Model. Acts (clicks, API calls, workflows). Core of autonomous agents |
| **ToolFormer** | LLM trained to decide when and how to use tools (APIs, calculators). Self-augmented intelligence |

---

## Mental Model Layer

|Layer|What it means|
|---|---|
| **LLM / GPT / MLM** | Core architecture |
| **SLM / MoE** | Scaling strategy |
| **VLM / SAM** | Modal expansion |
| **LRM / HRM** | Reasoning enhancement |
| **LAM / ToolFormer** | Action & tool usage |

---

## Practical Takeaways

- Use **GPT/LLM** → baseline
- Add **ToolFormer-style tool use** → real-world capability
- Add **LRM-style prompting** → reliability
- Consider **SLM** → cost optimization
- Add **VLM** only if needed

---

## Where Career Leverage Is

LAM + ToolFormer = **agents future**

LRM/HRM = where real progress is happening (reasoning > raw size)

SLMs will eat a lot of enterprise use-cases (cost > hype)