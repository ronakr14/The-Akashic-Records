```table-of-contents
```
## Design a batch pipeline that processes 50 TB of sales data every night within a 4-hour SLA.
Things interviewer expects:
* Partitioning strategy
* Parallelism
* Incremental processing
* Resource allocation
* Failure recovery
* Monitoring
Follow-up:
> What would you do if the job suddenly takes 7 hours?

The note is an interview-prep answer for designing a batch pipeline that processes 50 TB of nightly sales data within a 4-hour SLA (~3.5 GB/sec
  throughput), covering partitioning by sale_date + region (256 MB–1 GB files), incremental CDC/MERGE-based Bronze→Silver processing, Spark-on-K8s
  parallelism (200 workers, 3200 vCPU) with broadcast joins and shuffle optimization, idempotent checkpointed failure recovery with partition-level restart
  and DQ gates, and three-tier monitoring (infra, pipeline, data quality); the follow-up for a sudden 7-hour runtime walks through diagnosing data skew,
  small-file explosion, shuffle growth, and resource contention, then short-term fixes (horizontal scale, prioritize critical partitions) and long-term
  prevention (SLA alerts, skew detection, capacity planning).
  
---
## Design a batch architecture for a data lake where data arrives from:
* CRM
* ERP
* Mobile apps
* Third-party APIs
Requirements:
* Daily refresh
* Historical retention
* Data quality validation
* Schema evolution support

The note is an interview-prep answer for designing a daily-refresh batch data lake ingesting from CRM (Salesforce Bulk/incremental LastModifiedDate), ERP
  (CDC snapshots/exports), mobile apps (operational DB exports), and third-party APIs (Airflow-scheduled JSON pulls) — landing raw in cloud object storage
  (S3/ADLS/GCS) formatted as Iceberg/Delta for ACID, time-travel, schema evolution, and partition pruning; the architecture uses a Bronze (immutable raw,
  load_dt partitioned, forever retention for replay) → Silver (deduped, type-normalized, DQ-validated with quarantined failures) → Gold (BI/ML-ready) flow
  orchestrated by Airflow/Dagster, supports historical retention via SCD Type 2 master dimensions and daily snapshot tables for inventory, enforces quality
  gates (completeness, uniqueness, referential integrity, freshness, volume anomalies) via Great Expectations/Soda, and handles schema evolution through
  additive Iceberg/Delta changes, nullable backfill, a schema registry with compatibility rules, and monitoring across pipeline/data/cost metrics.
  
---
## Design a batch system that supports:
* Reprocessing historical data
* Backfills
* Auditability
* Data lineage
How would you organize:
* Raw layer
* Curated layer
* Metadata layer
The note is an interview-prep answer for designing a batch system supporting reprocessing, backfills, auditability, and lineage, organized into three
  layers: a Raw layer (append-only, immutable source data partitioned by load_date, tagged with batch_id/source_system/record_hash/load_timestamp, retained
  indefinitely for replay), a Curated layer split into Silver (deduped, validated, type-normalized trusted tables) and Gold (business-ready aggregates),
  with Iceberg/Delta versioning for time-travel and partition-scoped reruns (e.g. reprocess only sale_date=2025-01..03 for a tax bug, or backfill a new
  campaign_id column against 3 years of history in isolated backfill_run_* environments before promotion); a Metadata control plane (technical, operational,
  lineage, DQ, and audit tables like metadata.datasets, metadata.pipeline_runs, metadata.lineage, metadata.audit_log, metadata.dq_results) tools like
  OpenMetadata/DataHub/Apache Atlas captures column- and dataset-level lineage from CRM/ERP/Mobile → sales_fact → customer_360 → dashboards, with
  ingestion/transformation/DQ audit tables answering who loaded what, when, from which file, on which code version, and how many records passed or were
  rejected.

## See Also
- [[Distributed System]] — distributed systems foundations
- [[Data Lake]] — data lake architecture
- [[Delta Lake & Iceberg]] — lakehouse formats
- [[Batch Processing]] — batch processing patterns
- [[Stream Data Processing]] — stream processing