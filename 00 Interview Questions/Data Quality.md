---
type: question
---

```table-of-contents
```
## How would you validate a batch load before publishing it?
Possible checks:
* Row counts
* Null checks
* Referential integrity
* Distribution checks
* Freshness checks

Pre-publish validation, layered:
* **Volume** — row count vs expected range (alert on ±X% deviation), file count, bytes written. Catches truncation and duplication.
* **Schema** — column types, nullability, new/missing columns. Block on breaking changes; warn on additive.
* **Null checks** — null rate per critical column; alert when null rate spikes vs 7-day baseline.
* **Uniqueness** — primary key uniqueness, business key uniqueness.
* **Referential integrity** — every FK exists in the referenced table; orphan rate < threshold.
* **Distribution** — min/max/mean/quantiles vs historical baseline (e.g. order value p99). Catches silent unit-conversion bugs.
* **Freshness** — max event timestamp is within SLA of wall clock; data covers the expected window with no gaps.
* **Reconciliation** — sum/count of key metrics matches source system report (control totals).
* **Sampling** — spot-check 1–5% of rows against source for correctness.

Gate the publish: fail the job (or quarantine to a `quarantine/` path) if any blocking check fails. Surface results in a DQ dashboard with trend lines.

---
## A batch job completes successfully but produces incorrect numbers.
How would you detect and prevent this?

Detection:
* **Pre-publish DQ gates** — every job has row-count, null-rate, distribution, and reconciliation checks; the job *fails* (doesn't just warn) on a check that breaches threshold.
* **Reconciliation vs source-of-truth** — daily control totals (e.g. source ERP's reported revenue) compared to pipeline output. Even small mismatches caught.
* **Data diff vs prior run** — automated comparison of yesterday vs today on key metrics. Catches silent unit/filter regressions.
* **Anomaly detection** — p99 of order_value, count of new customers, etc. Monitored; alert on >3σ from rolling baseline.
* **Downstream freshness** — dashboards show "data as of" timestamp; if a value is suspiciously stale, the pipeline didn't run correctly.
* **Sampling/spot-audits** — humans (or QA) inspect 1–5% of rows.

Prevention:
* **Tests in CI** — schema, distribution, reconciliation tests run on every code change.
* **Data contracts** — schema and semantics validated at ingest.
* **Idempotent + atomic writes** — partial writes never visible.
* **Quarantine, not silent success** — bad rows routed to `/quarantine/` with reason; report surfaces quarantine rate.
* **Versioned outputs** — roll forward/back by version swap.
* **Codify the "definition of correct"** — for every business metric, a clear spec (input, transformation, expected output) reviewed by domain owner.

Refer: [[Data Quality]]

---
## How would you design automated data quality gates in a batch pipeline?

Architecture:
* **Per-table DQ contract** — list of checks (row count range, null rate, uniqueness, FK integrity, distribution, freshness, reconciliation). Owned by data steward.
* **Layered enforcement:**
  * **In-pipeline** — every transform emits metrics; thresholds block publish if breached.
  * **Post-write** — separate DQ job reads the output and runs checks; result gates downstream promotion.
  * **Continuous** — independent observer job samples and validates throughout the day.
* **Blocking vs warning** — define severity per check: blocking = fail job; warning = alert but allow.
* **Quarantine path** — bad rows go to `/quarantine/yyyy-mm-dd/`, not dropped. Pipeline still publishes clean rows.
* **Trend storage** — check results stored in time-series DB; dashboards show 30-day trend.
* **Tooling** — Great Expectations, Soda Core, Monte Carlo, Bigeye, dbt tests for SQL-pipeline cases.
* **What to alert on** — check failure, check degradation (p99 worse than baseline), check drift (threshold of "passing" checks trending down).
* **CI integration** — checks registered as code; PR that removes a check requires approval.

Refer: [[Data Quality]]
