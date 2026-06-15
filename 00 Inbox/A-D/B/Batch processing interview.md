```table-of-contents
```
# System Design
## Design a batch pipeline that processes 50 TB of sales data every night within a 4-hour SLA.
Things interviewer expects:
* Partitioning strategy
* Parallelism
* Incremental processing
* Resource allocation
* Failure recoverya
* Monitoring
Follow-up:
> What would you do if the job suddenly takes 7 hours?
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
---
# Incremental Processing
## 4. You have a 100 TB table.
A full reload takes 15 hours.
How would you implement incremental loading?
Expected discussion:
* Watermarks
* High-water marks
* CDC
* Timestamp-based extraction
* Idempotency
---
## 5. What can go wrong with timestamp-based incremental loads?
Look for:
* Clock drift
* Late arriving records
* Timezone issues
* Duplicate processing
* Missing records
---
## 6. Explain how you would backfill one year of historical data without impacting production batch jobs.
---
# Partitioning
## 7. A daily batch job scans 30 TB but only processes one day of data.
How would you optimize it?
Expected:
* Partition pruning
* Predicate pushdown
* File layout optimization
---
## 8. How would you choose partition keys for:
* Orders table
* Customer table
* IoT sensor table
Why?
---
## 9. What problems occur when partitions become too small?
---
## 10. What problems occur when partitions become too large?
---
# Data Quality
## 11. How would you validate a batch load before publishing it?
Possible checks:
* Row counts
* Null checks
* Referential integrity
* Distribution checks
* Freshness checks
---
## 12. A batch job completes successfully but produces incorrect numbers.
How would you detect and prevent this?

---
## 13. How would you design automated data quality gates in a batch pipeline?
---
# Failure Recovery
## 14. A batch pipeline has 20 steps.
Step 19 fails after processing 8 hours.
What would you do?
Expected:
* Checkpointing
* Restartability
* Intermediate storage
---
## 15. Explain the difference between:
* Retry
* Resume
* Restart
* Reprocess
---
## 16. How do you make batch jobs idempotent?
One of the most common senior-level questions

---
# Performance Optimization
## 17. A Spark batch job slowed from 45 minutes to 3 hours.
How would you investigate?
Potential areas:
* Data growth
* Skew
* Shuffle size
* Join strategy
* Cluster changes
---
## 18. A batch job processes:
```text
1 billion records
20 joins
10 aggregations
```
How would you optimize it?

---
## 19. How do you identify bottlenecks in a batch workload?
Expected:
* CPU
* Memory
* Network
* Disk I/O
* Shuffle
---
## 20. Explain predicate pushdown and why it matters in batch processing.
---
# Metadata & Observability
Since you work in data engineering and have been exploring metadata-driven optimization, these questions are increasingly common.
## 21. What metadata would you collect from every batch job?
Possible answer:
```json
{
  "job_id": "",
  "runtime_sec": 0,
  "records_read": 0,
  "records_written": 0,
  "partitions_scanned": [],
  "bytes_processed": 0,
  "error_count": 0
}
```
---
## 22. How would you identify inefficient batch jobs automatically?
---
## 23. What telemetry signals would help predict SLA violations before they happen?
---
## 24. Design a metadata-driven batch optimization platform.
This is a Staff-level question.

---
# Query Optimization
## 25. A query reads 10 TB to return 100 rows.
Why might this happen?

---
## 26. Given a query plan, how would you identify:
* Expensive joins
* Full table scans
* Data skew
* Excessive shuffles
---
## 27. What information would you extract from query plans to build an AI optimization engine?
Interesting for your lakehouse optimization work.
Possible features:
```json
{
  "join_count": 3,
  "join_types": ["inner", "left"],
  "estimated_rows": 1000000,
  "scan_bytes": 50000000000,
  "group_by_count": 2
}
```
---
# Lakehouse-Specific Questions
## 28. Why is file size important in batch processing?
---
## 29. What problems do small files create?
Expected:
* Metadata overhead
* Slow planning
* Inefficient scans
---
## 30. How would you compact files in a data lake?
---
## 31. Explain how partition pruning works in a lakehouse.
---
## 32. How would you detect that a table requires compaction?
---
# Advanced Scenario Questions
## 33. A batch pipeline that normally processes 500 GB suddenly receives 20 TB.
What happens?
How would you prevent failures?

---
## 34. Your nightly batch SLA is 3 hours.
Business now requires 1 hour.
What architectural changes would you consider?

---
## 35. You discover that yesterday's batch produced incorrect results.
Downstream dashboards have already consumed the data.
Walk me through your incident response process.

---
## 36. Design a batch processing framework from scratch.
Requirements:
* Scheduling
* Dependency management
* Retries
* Metadata collection
* Data quality
* Observability
* Cost optimization
---
# Staff/Principal-Level Questions
## 37. If you could collect only 10 metrics from every batch job, which would you choose and why?
---
## 38. How would you build an AI system that recommends batch optimizations automatically?
treat it as a **closed-loop optimization platform** rather than a simple recommendation engine.
The goal is:

> Observe → Diagnose → Recommend → Validate → Learn

High level
---
## 39. How would you estimate the cost of a batch workload before execution?
---
## 40. How would you predict batch job runtime using historical telemetry?
Inputs might include:
```json
{
  "rows_scanned": 500000000,
  "join_count": 4,
  "shuffle_gb": 120,
  "partition_count": 250
}
```
---
## 41. Design a self-tuning batch platform that automatically:
* Detects slow jobs
* Recommends optimizations
* Applies safe optimizations
* Measures improvement
