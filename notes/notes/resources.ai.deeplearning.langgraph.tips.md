---
id: v6vfc8hv7fnqsjan4k0fv4e
title: Tips
desc: ''
updated: 1752507895814
created: 1752507895463
---

## 🎩 Pro Ops Tips

* Use **state dicts** as your data carrier between nodes.
* Nodes can be entire LLM chains, not just single steps.
* Log transitions to visualize execution flow (use graphviz).
* Avoid single mega-graphs. Build **modular subgraphs** and compose.
* Handle exceptions inside nodes; define fallback edges where needed.
