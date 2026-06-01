#data-engineering #fundamentals
# The 15 Truths That Change the Game

1. **Batch vs. Streaming Ingestion**
    - Batch: Think nightly CSV ingestion via Airflow into Snowflake—solid for predictable bulk loads, terrible for real-time.
    - Streaming: Kafka + Flink feeding low-latency dashboards. Powerful, but a beast to scale.
2. **Change Data Capture (CDC)** Skip full table reloads—stream only data mutations (INSERT/UPDATE/DELETE). Efficient and real-time reactive.
3. **Idempotency** Let failures happen—they will. But make operations replay-safe so multiple runs don’t corrupt your state. Fidelity saved here = debugging joy.
4. **OLTP vs. OLAP** OLTP = transaction-heavy, low-latency systems (PostgreSQL, DynamoDB). OLAP = analytical heavy-lifters (Snowflake, BigQuery). Each serves a different beast—don’t swap ’em.
5. **Row-Based vs. Columnar Storage** Row-based is great for transactions, writes, updates. Columnar is analytical gold—fast aggregations, compressed reads.
6. **Partitioning** Chunking data by date or other keys slims reads and speeds queries. It’s table-level Tetris.
7. **ETL vs. ELT**
    - ETL: transform before load—classic, controlled, but slower.
    - ELT: dump raw data into warehouse, transform later—modern, flexible, and faster.
8. **CAP Theorem** Consistency, Availability, Partition Tolerance—you get two. Pick strategically (e.g. CP for orders, AP for searches).
9. **Windowing in Streaming** Slice streams into tumbling, sliding, session, or count windows. Vital for real-time analytics and aggregation.
10. **DAGs & Workflow Orchestration** Orchestrate jobs with DAGs to keep pipelines sane and ordered. Tools: Airflow, Prefect, Dagster.
11. **Retry & Dead-Letter Queues (DLQs)** Expect glitches. Automate retries, and quarantine failed events in DLQs—so bad data doesn’t burn everything.
12. **Backfilling & Reprocessing** Data bugs or downtime? Re-run logic (reprocess) or fill missing data ranges (backfill). Always plan for makeup ops.
13. **Data Governance** Data must be available, accurate, consistent, secure, and compliant. It’s not optional—legal and trust depend on it.
14. **Time Travel & Versioning** Query your data as of yesterday—or last week. Think Git for your tables. Essential for auditability and reproducibility.
15. **Distributed Processing Fundamentals**
	- Partitioning & bucketing: split data sensibly.
	- Mitigate **data skew** with salting or broadcast joins.
	- Understand **shuffling**—it costs performance when data moves across nodes.