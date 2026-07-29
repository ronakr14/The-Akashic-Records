# AI Summary
Data Engineering — 15 Core Truths. 1. **Batch vs Streaming**

```table-of-contents
```

# Data Engineering — 15 Core Truths

## Ingestion

1. **Batch vs Streaming**
   - **Batch**: Nightly CSV loads via [[Airflow]] into [[Snowflake]] — solid for predictable bulk loads, terrible for real-time.
   - **Streaming**: [[Kafka]] + [[Flink]] feeding low-latency dashboards. Powerful, but operationally complex at scale.

2. **Change Data Capture ([[CDC]])**
   Skip full table reloads — stream only mutations (INSERT/UPDATE/DELETE). Efficient and real-time reactive. Tools: Debezium, AWS DMS.

3. **Windowing in Streaming**
   Slice streams into tumbling, sliding, session, or count windows. Vital for real-time analytics and aggregation.

## Storage & Formats

4. **Row-Based vs Columnar Storage**
   Row-based: good for transactions, writes, updates ([[PostgreSQL]], [[DynamoDB]]). Columnar: analytical gold — fast aggregations, compressed reads ([[Parquet]], [[Snowflake]], [[BigQuery]]).

5. **Partitioning & Bucketing**
   Chunk data by date or other keys to slim reads and speeds queries. Combine with bucketing for high-cardinality columns. Avoid over-partitioning — too many small files hurt performance.

6. **Time Travel & Versioning**
   Query data as of a past point in time — Git for tables. Supported natively in [[Delta Lake]], [[Apache Iceberg]], [[Snowflake]]. Essential for auditability and reproducibility.

## Processing

7. **ETL vs ELT**
   - **ETL**: transform before load — classic, controlled, slower.
   - **ELT**: load raw, transform in-warehouse — modern, flexible, leverages compute of the target system.

8. **[[DAGs]] & Workflow Orchestration**
   Orchestrate jobs with DAGs to keep pipelines ordered and observable. Tools: [[Airflow]], Prefect, Dagster.

9. **Retry & Dead-Letter Queues ([[DLQ]])**
   Expect failures. Automate retries with backoff, and quarantine failed events in DLQs so bad data doesn't poison downstream consumers.

10. **Backfilling & Reprocessing**
    Data bugs or downtime? Re-run logic (reprocess) or fill missing ranges (backfill). Always design pipelines to be re-runnable.

11. **Distributed Processing Fundamentals**
    - Partitioning & bucketing: split data sensibly across nodes.
    - Mitigate **data skew** with salting or broadcast joins.
    - Minimize **shuffling** — data movement across nodes is the primary performance bottleneck.

## Architecture

12. **[[OLTP]] vs [[OLAP]]**
    OLTP: transaction-heavy, low-latency ([[PostgreSQL]], [[DynamoDB]]). OLAP: analytical heavy-lifters ([[Snowflake]], [[BigQuery]], [[Redshift]]). Different engines for different workloads — don't substitute one for the other.

13. **[[CAP Theorem]]**
    Consistency, Availability, Partition Tolerance — pick two. CP for orders and payments, AP for search and recommendations. Understand what your system sacrifices.

## Quality & Governance

14. **[[Idempotency]]**
    Make operations replay-safe so multiple runs don't corrupt state. Use deterministic keys, upsert semantics, and deduplication. The single most important property for reliable pipelines.

15. **Data Governance**
    Data must be available, accurate, consistent, secure, and compliant. Covers lineage, access control, PII handling, retention policies, and audit trails. Not optional — legal and trust depend on it.
