---
domain: data-engineering
subdomain: data-processing
source_type: self
note_type: interview
status: evergreen
level: advanced
tags:
  - etl
---
# AI Summary
Comprehensive Data Engineering interview preparation guide covering 30 ETL and ELT interview questions from beginner to senior architect level. Topics include ETL fundamentals, incremental loading, CDC, Slowly Changing Dimensions, idempotency, late-arriving data, data quality, governance, distributed ETL with Spark, partitioning, data skew, metadata-driven frameworks, lakehouse architecture, monitoring, and modern ETL platform design. Includes expected discussion points, SQL examples, architecture questions, and references to related concepts for structured interview study.

---
# Level 1: Fundamentals
### 1. What are the differences between ETL and ELT?
**Looking for:**
* Transformation location
* Compute considerations
* Modern cloud patterns
* Trade-offs
---
### 2. What are the main stages of an ETL pipeline?
Expected:
* Extract
* Transform
* Load
Bonus:
* Validation
* Monitoring
* Recovery
---
### 3. How would you handle duplicate records during ETL?
Looking for:
* Primary keys
* Hash-based deduplication
* Window functions
* CDC awareness
Example:
```sql
ROW_NUMBER() OVER (
  PARTITION BY customer_id
  ORDER BY updated_at DESC
)
```
---
### 4. Difference between full load and incremental load?
Expected discussion:
| Full Load    | Incremental  |
| ------------ | ------------ |
| Entire table | Only changes |
| Expensive    | Efficient    |
| Simple       | Complex      |
---
# Level 2: Intermediate ETL Engineering
### 5. How would you design an ETL pipeline for a 500GB source table that updates daily?
Topics:
* Partitioning
* Incremental loads
* CDC
* Parallel processing
Bad answer:
> Reload everything.
Good answer:
> Capture only changed records using CDC or watermarking.
---
### 6. Explain Slowly Changing Dimensions (SCD).
Should discuss:
* Type 1
* Type 2
* Type 3
Example:
Customer changes city.
Type 1:
```
Overwrite
```
Type 2:
```
Create new version
```
Type 3:
```
Keep previous value
```
---
### 7. How do you implement SCD Type 2 efficiently?
Looking for:
* Surrogate keys
* Effective dates
* Current flags
Example schema:
```sql
customer_sk
customer_id
city
effective_from
effective_to
is_current
```
---
### 8. What is Change Data Capture (CDC)?
Expected:
* INSERT
* UPDATE
* DELETE tracking
Methods:
* Timestamp
* Database logs
* Debezium
* Replication streams
---
# Level 3: Production ETL Challenges
### 9. A daily ETL job suddenly takes 8 hours instead of 30 minutes. How do you investigate?
Strong answer covers:
* Data volume growth
* Query plans
* Partition pruning
* Resource contention
* Skew
* Network bottlenecks
---
### 10. How do you make ETL pipelines idempotent?
A favorite senior-level question.
Meaning:
Running pipeline multiple times should produce same result.
Techniques:
* MERGE
* UPSERT
* Deduplication
* Atomic writes
---
### 11. How do you recover from ETL failures?
Topics:
* Checkpointing
* Retry logic
* Dead letter queues
* Reprocessing
---
### 12. How would you handle late-arriving data?
Example:
Order arrives 3 days late.
Discussion:
* Watermarks
* Reprocessing windows
* Backfills
---
# Level 4: Data Quality & Governance
### 13. How do you validate source data before loading?
Possible checks:
```text
Null checks
Range checks
Referential integrity
Duplicate checks
Schema validation
```
---
### 14. How would you detect silent data corruption?
Looking for:
* Row counts
* Checksums
* Hash totals
* Data contracts
Example:
```sql
MD5(concatenated_columns)
```
---
### 15. What metrics would you monitor for ETL pipelines?
Strong answer:
Business metrics
* Orders processed
* Revenue totals
Technical metrics
* Runtime
* Failure rate
* Throughput
* Data freshness
---
### 16. How would you design data lineage for ETL?
Should discuss:
* Source tracking
* Transformation tracking
* Column lineage
* Auditability
---
# Level 5: Big Data ETL
### 17. How would you ETL 10TB of data daily?
Topics:
* Distributed processing
* Spark
* Partitioning
* Parallelism
Expected tools:
* Apache Spark
* Apache Flink
---
### 18. Explain partitioning and bucketing.
Looking for:
Partitioning:
```
year=2026/month=06/day=02
```
Bucketing:
```
hash(customer_id)%100
```
---
### 19. What causes data skew and how do you solve it?
Example:
```
80% records belong to one customer
```
Solutions:
* Salting
* Repartitioning
* Adaptive execution
---
### 20. How would you optimize a large ETL join?
Looking for:
* Broadcast joins
* Partition alignment
* Join order
* Statistics
---
# Architecture Questions
### 21. Design an ETL platform for 1000 source systems.
Expect discussion around:
* Metadata-driven pipelines
* Orchestration
* Reusable framework
* Monitoring
---
### 22. ETL pipeline for real-time fraud detection?
Topics:
* Streaming
* CDC
* Event-driven architecture
Tools:
* Apache Kafka
* Apache Flink
---
### 23. Design ETL for a Data Lakehouse.
Expected:
```
Bronze
  ↓
Silver
  ↓
Gold
```
Bronze:
Raw data
Silver:
Cleaned data
Gold:
Business-ready data
---
### 24. How would you implement schema evolution?
Examples:
* New columns
* Renamed columns
* Deleted columns
Should discuss:
* Backward compatibility
* Metadata management
---
# Very Strong Senior-Level Questions
### 25. When would you intentionally choose ETL over ELT?
Good answers:
* PII masking
* Compliance
* Cost control
* Legacy systems
---
### 26. What is the difference between data correctness and data completeness?
Correctness:
```text
Value is accurate
```
Completeness:
```text
All records are present
```
---
### 27. How do you guarantee exactly-once processing?
Topics:
* Idempotency
* Checkpointing
* Transactional writes
---
### 28. How would you backfill 2 years of historical data without impacting production?
Looking for:
* Separate compute clusters
* Batch windows
* Incremental merge
---
### 29. Describe a metadata-driven ETL framework.
A senior engineer should discuss:
```text
Pipeline definitions stored in metadata
Dynamic execution
Reusable transformations
Central monitoring
```
---
### 30. If you were building ETL from scratch today, what architecture would you choose and why?
A strong 2026 answer often includes:
```text
Source Systems
    ↓
CDC
    ↓
Kafka
    ↓
Bronze Layer
    ↓
Spark/dbt
    ↓
Silver Layer
    ↓
Gold Layer
    ↓
BI / ML
```
Using technologies such as:
* Apache Kafka
* Databricks
* dbt
* Apache Airflow

## See Also
- [[ETL vs ELT]] — decision framework: when to choose ETL vs ELT
- [[ETL]] — ETL pattern reference
- [[ELT (Extract, Load, Transform)]] — ELT pattern reference
- [[Incremental Data Loading Strategies]] — incremental loading patterns
- [[Batch Processing]] — batch processing overview
