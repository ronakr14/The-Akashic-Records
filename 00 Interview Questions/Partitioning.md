```table-of-contents
```
## A daily batch job scans 30 TB but only processes one day of data.
How would you optimize it?
Expected: `Partition pruning, Predicate pushdown, File layout optimization`

If a daily batch job scans 30 TB but only processes one day's data, I'd first check whether partition pruning is working. The table should be partitioned on the date column being filtered. Next, I'd ensure predicates are pushdown-friendly and avoid functions on partition columns. I'd optimize file layout by using Parquet, compacting small files, and clustering data on frequently filtered columns. I'd also avoid `SELECT *` and verify improvements using EXPLAIN plans and scan metrics. The goal is to reduce data scanned from tens of terabytes to only the partitions, files, and columns required for that day's processing.

Refer: [[Partition Strategy]]

---
## How would you choose partition keys for:
* Orders table
* Customer table
* IoT sensor table
Why?
---
## What problems occur when partitions become too small?
---
## What problems occur when partitions become too large?