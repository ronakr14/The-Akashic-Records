---
type: question
---

```table-of-contents
```
## What is a data contract and how does it apply to batch pipelines?
A data contract is an agreement between producer and consumer on schema, semantics, SLAs, and ownership — written, versioned, enforced at the ingest boundary (not after the fact).
* **Schema** — column names, types, nullability, allowed values.
* **Semantics** — definition of `revenue`, granularity of `order_id`, partition semantics.
* **SLA** — max lag, max volume, max null rate. Producer owns; consumer can break the contract by changing query semantics.
* **Ownership** — named team accountable for changes.
* **Enforcement** — schema registry (Protobuf/Avro) + automated validation in the ingest job. Breaking changes require versioned migration.
* **Why it matters for batch** — eliminates the "silent schema drift at 3am" class of incidents. Turns tribal knowledge into a CI-enforced artifact.
* **Tools** — DataHub, Great Expectations, Protobuf Schema Registry, Open Data Contract Standard (ODCS).

## How would you attribute batch pipeline cost to teams, products, or business units?
FinOps for data. Every pipeline run emits cost metadata, rolled up by ownership tag.
* **Tag at submission** — `team`, `product`, `cost_center`, `pipeline_owner`, `env`. Tags flow through orchestrator → cluster → warehouse query history.
* **Compute cost** — `cluster_seconds × instance_price × utilization` for Spark/Flink; `credits_used × credit_price` for Snowflake/BigQuery; `DPU-seconds` for Databricks.
* **Storage cost** — bytes stored per layer (raw/curated/sandbox), tagged by producer team.
* **Roll-up dashboard** — daily/weekly spend per team; anomaly alerts on >X% deviation.
* **Chargeback / showback** — bill owners; budget enforcement at pipeline level (kill if team exceeds monthly budget).
* **Per-row cost** — `cost / rows_written` = unit economics; identify pipelines that are expensive per record (likely candidates for optimization or deletion).
* **Tooling** — CloudZero, Vantage, Apptio for cloud FinOps; DataHub + dbt for lineage-driven cost attribution.

## What testing strategies are essential for batch pipelines?
* **Unit tests** — transformation logic on fixture data; mocked sources.
* **Schema tests** — every output table has expected schema; dbt's `not_null`, `unique`, `accepted_values`.
* **Data tests** — value distributions, referential integrity, freshness, volume. Great Expectations, Soda Core, dbt tests.
* **Contract tests** — producer schema matches consumer expectations (DataHub, Schema Registry).
* **Data diff tests** — compare today's output vs yesterday's, on key metrics (count, sum, hash of sample). Catches silent regressions even when tests pass.
* **Replay tests** — re-run pipeline against historical inputs; assert output matches a frozen golden dataset.
* **SLA tests** — pipeline completes within time budget on a representative input.
* **Failure tests** — inject failures (bad rows, missing partitions, slow sources); assert pipeline fails gracefully, doesn't corrupt downstream.
* **End-to-end** — small synthetic dataset traverses the entire pipeline; verify final output.
* **CI/CD** — tests run on PR; a SQL change that breaks a test blocks merge.

Refer: [[Data Quality]]

## How would you handle PII and sensitive data in a batch pipeline?
* **Classify at ingest** — tag columns as `public | internal | confidential | restricted | pii | phi` using automated scanners (BigQuery DLP, AWS Macie, Presidio).
* **Mask early** — apply masking/tokenization in the staging layer, not the curated layer. Once PII lands in curated tables, auditability gets hard.
* **Tokenization** — replace PII with a token; store real values in a separate, access-controlled vault. Joins still work.
* **Deterministic hashing** — for join keys, use HMAC with a rotating salt. Reversible only by the vault service.
* **Row/column-level security** — engine-native (BigQuery row access policies, Snowflake row access policies, Iceberg hidden partitions) so downstream consumers never see unauthorized rows.
* **Access logging** — every PII column read goes to an audit log; alert on bulk reads.
* **Retention** — auto-delete raw PII after N days; keep aggregates longer.
* **Compliance** — GDPR right-to-erasure requires pipeline to reprocess affected partition; design partitions to be rewritable per-subject.
* **Interview framing** — show you understand that "security" isn't just encryption at rest; it's classification → masking → access control → audit.

## Explain data lineage and how you'd implement it for a batch platform.
Lineage = graph of where data came from, what transformed it, and where it went.
* **Two kinds:**
  * **Technical lineage** — table-to-table, column-level. Parsed from query logs, dbt manifests, Spark plans.
  * **Business lineage** — dataset → dashboard → business decision. Owned by data steward.
* **Capture at execution time**, not declaratively — actual lineage reflects what ran, not what was intended.
* **OpenLineage + Marquez** — open standard; Spark/Dbt/Airflow emit events; Marquez stores the graph. Avoid vendor lock-in.
* **Use cases:**
  * Impact analysis — "what breaks if I change this column?"
  * Root cause — "which upstream source caused the bad number?"
  * Compliance — "where did this PII flow?"
  * Cost attribution — "which downstream dashboards depend on this expensive pipeline?"
* **Failure modes** — declared lineage that drifts from reality; missing column-level granularity; lineage for legacy jobs you can't instrument.
Refer: [[Data Lineage]]

## Compare modern orchestrators: Airflow vs Dagster vs Prefect vs Spark declarative.
| Dimension | Airflow | Dagster | Prefect | Spark Declarative |
|---|---|---|---|---|
| Model | DAG of tasks | Asset/data-centric | Task-centric, dynamic | Pipeline-of-pipelines (DLT) |
| Sweet spot | Mature, ops-heavy teams | Data + ML teams | Python-first, quick start | ETL on Databricks |
| Lineage | Plugin (OpenLineage) | First-class asset graph | Limited | First-class |
| Testing | Workable, slow | First-class (asset checks) | First-class | Built-in expectations |
| Backfills | Manual or plugin | First-class partition backfills | First-class | First-class |
| Dynamic | Limited | Strong (sensor assets) | Strong (subflows) | Limited |
| Footprint | Heavy (scheduler + workers) | Lighter | Lightest | Spark-bound |
| Interview angle | "Mature, but lineage/backfills need work" | "Asset model matches how data teams think" | "Fastest to ship" | "Best if you're already on Databricks" |

Choice depends on team maturity and whether you think in tasks or assets.

## What FinOps levers are unique to batch workloads?
* **Right-sizing executors** — pick executor count from telemetry, not over-provisioning.
* **Spot/preemptible for non-urgent** — ETL workloads can tolerate preemption; ML training usually can't.
* **Auto-suspend / auto-terminate** — dev clusters off at night; warehouses auto-suspend after 5min idle.
* **Tiered storage** — hot data on standard, warm on infrequent access, cold on Glacier/Archive. Most lakehouses are 80% cold.
* **Photonic / Photon accelerators** — engine-level speedup = direct cost cut for the same workload.
* **Result caching** — repeated queries hit cache. BigQuery/Snowflake handle this; Spark needs manual broadcast caching.
* **Cluster sharing** — pool multiple small jobs on one long-lived cluster instead of cold-starting per job.
* **Schedule shift** — move batch to off-peak for spot discount or region with cheaper compute.
* **Delete unused** — tables no one queried in 90 days → archive or drop. Most orgs find 30–50% of storage is orphaned.
* **Tag everything** — untagged cost is untrackable cost.

## How do you design a batch pipeline to support safe rollbacks?
* **Versioned writes** — every output to `/table/dt=YYYY-MM-DD/v=run_id/`. Old versions remain queryable.
* **View/table swap, not overwrite** — atomically point a view at the latest version; never overwrite the active partition in place.
* **Code + config versioning** — every run records the git SHA of pipeline code and config; roll back means re-running with old code.
* **Data diff at promotion** — promote a new version only after automated comparison vs current.
* **Read-side compatibility** — consumers query a versioned view, never the raw path; they tolerate version flips.
* **Rollback playbook** — documented: detect → freeze downstream → swap to last-good version → notify → root-cause.
* **Blue/green for big releases** — write new version in parallel; switch view only after validation.
* **Why most teams fail** — they overwrite partitions in place; once bad data is in, rollback = rerun everything.

## See Also
- [[Batch Processing]] — batch processing overview
- [[Stream Data Processing]] — when streaming beats batch
- [[Idempotency]] — making pipelines retry-safe
- [[Incremental Load Strategy]] — incremental loading patterns
- [[Data Modelling]] — data modelling principles