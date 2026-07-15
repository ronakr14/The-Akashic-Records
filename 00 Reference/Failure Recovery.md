```table-of-contents
```
## A batch pipeline has 20 steps.
Step 19 fails after processing 8 hours.
What would you do?
Expected:
* Checkpointing
* Restartability
* Intermediate storage

Decision tree:
* **Don't restart from step 1.** That's the default trap.
* **Is step 19 idempotent and isolated?** — Yes: restart from step 19. No: investigate before retry.
* **Is intermediate state preserved?** — Each step should write to a versioned path (`/curated/orders/dt=2026-06-18/v=2026-06-18T08:00:00/`). With versioned writes, step 19 can re-read its inputs without rerunning 1–18.
* **Diagnose first** — check logs, metrics, the failing record (sample input to step 19). Is it data (bad row, null in required field) or infra (OOM, timeout, lost executor)? 8 hours in usually means data drift or capacity, not code.
* **Three options:**
  1. **Resume** from step 19 if inputs are intact and failure is transient (retry once with backoff).
  2. **Restart** from step 19 if inputs are intact but failure is deterministic; fix the cause first.
  3. **Reprocess** affected inputs only — replay the failed step's input slice if it was scoped; otherwise rollback to last good checkpoint.
* **Architecture that prevents this question:**
  * Each step writes to versioned, immutable paths.
  * Watermark/checkpoint per step (last successful run ID).
  * Idempotent step semantics (safe to rerun any step any time).
  * Orchestrator (Airflow/Dagster) that retries only the failed task and resumes downstream.
  * Intermediate storage between every expensive step, so 1–18 outputs aren't wasted.
* **Post-mortem** — add a regression test, add monitoring for the failing condition, document the checkpoint map.

Refer: [[Idempotency]]

---
## Explain the difference between:
* Retry
* Resume
* Restart
* Reprocess

* **Retry** — re-attempt the *same instance* of a failed step, same inputs, same code, no state change. Used for transient failures (network blip, deadlock, leader election). Cheap, bounded (max 3 attempts). Doesn't apply if the step partially completed and wrote some output.
* **Resume** — pick up a step (or pipeline) from its *last checkpoint*; some state already exists, the step continues from there. Requires the step to be idempotent and to have a persisted checkpoint (e.g. Spark task re-execution, Airflow `latest_only`, partition offset).
* **Restart** — re-run a step (or pipeline) from scratch; discard intermediate state, re-execute from the beginning of that step. Used when state is corrupt, code changed, or failure was deterministic. Inputs to the step must still be available.
* **Reprocess** — re-execute over a *historical time window* (e.g. re-run last 30 days) to fix a bad output, even though the run was previously "successful". Most expensive; involves recomputation and downstream data corrections. Often done via backfill.

Hierarchy of cost: `retry < resume < restart < reprocess`. Choose the cheapest that achieves correctness.

---
## How do you make batch jobs idempotent?

I make batch jobs idempotent by ensuring reruns produce the same final state. Common techniques include partition overwrite for full partition loads, MERGE/UPSERT operations for incremental loads, deduplication using business keys, atomic writes, and careful watermark management. I also use staging tables, audit tables, and batch run tracking so failed jobs can be safely retried without creating duplicates or data loss. The key principle is that a retry should leave the target dataset in exactly the same state as a successful first run.

## See Also
- [[Idempotency]] — idempotency deep-dive
- [[Batch Processing]] — batch processing patterns
- [[Incremental Load Strategy]] — incremental loading