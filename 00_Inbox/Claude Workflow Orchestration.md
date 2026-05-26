# Claude Workflow Orchestration

## Summary
Hacks and strategies for maximizing Claude context efficiency and orchestrating complex workflows. Covers subagent strategy, self-improvement loops, verification practices, and task management.

## Tags
#type/note #area/personal #status/done

---

## Context Token Hacks

1. Disconnect MCP servers — keep only what's needed
2. Keep `claude.md` under 200 lines
3. Use plan mode before every non-trivial task
4. Auto-compact triggers at 95% capacity
5. Sonnet for coding, Haiku for subagents, Opus for planning
6. Avoid subagents during peak hours

---

## Workflow Orchestration

### Plan Node Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan — don't keep pushing
- Write detailed specs upfront to reduce ambiguity

### Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- One task per subagent for focused execution

### Self-Improvement Loop
- After ANY correction: update `tasks/lessons.md` with the pattern
- Write rules that prevent the same mistake
- Review lessons at session start for relevant project

### Verification Before Done
- Never mark task complete without proving it works
- Ask: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### Demand Elegance (Balanced)
- For non-trivial changes: ask "is there a more elegant way?"
- If a fix feels hacky: implement the elegant solution
- Skip this for simple fixes — don't over-engineer

### Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from user

---

## Task Management

1. **Plan First** — Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan** — Check in before starting implementation
3. **Track Progress** — Mark items complete as you go
4. **Explain Changes** — High-level summary at each step
5. **Document Results** — Add review section to `tasks/todo.md`
6. **Capture Lessons** — Update `tasks/lessons.md` after corrections

---

## Core Principles

- **Simplicity First** — Make every change as simple as possible
- **No Laziness** — Find root causes. No temporary fixes
- **Minimal Impact** — Changes should only touch what's necessary