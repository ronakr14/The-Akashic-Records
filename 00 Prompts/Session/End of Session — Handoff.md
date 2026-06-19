---
description: End-of-session prompt — write a handoff.md capturing goal, state, active files, failures, next step.
use_when: Before closing a long Claude session.
inputs: [full session context]
outputs: handoff.md
related: [[Feedback — Extract]]
tags: [prompt, session, handoff, memory]
---
```table-of-contents
```
Before we end this session, write a `handoff.md` file that captures:

- the goal we're working toward
- current state of the repo
- files you're actively editing
- everything you've tried that failed
- the next step you'd take

---

Related: [[Feedback — Extract]] — pull session corrections into a reusable file. [[Daily Note — Update]] — log a one-liner summary.