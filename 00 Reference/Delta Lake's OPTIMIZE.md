# Delta Lake's OPTIMIZE

```table-of-contents
```

> This is one of the most misunderstood areas in Delta Lake.
>
> Many engineers think:
>
> ```sql
> OPTIMIZE table
> ```
>
> means:
>
> ```
> Merge small files together
> ```
>
> That's only about 30% of what is happening.

---

## Why OPTIMIZE Exists

Imagine your streaming pipeline writes:

```text
5 MB
10 MB
8 MB
12 MB
7 MB
...
```

After a month:

```text
100,000 files
```

Total data:

```text
1 TB
```

Average file size:

```text
10 MB
```

This is a disaster.

Before Spark reads data, it must:

```text
List files
Open files
Read metadata
Create tasks
Schedule tasks
```

100,000 files creates huge overhead even before processing begins. Small-file proliferation is a major performance problem in lakehouses. ([docs.databricks.com](https://docs.databricks.com/aws/en/delta/tune-file-size?utm_source=chatgpt.com "Control data file size | Databricks on AWS"))

→ **Risk:** Without OPTIMIZE, streaming pipelines degrade over time. Query latency grows linearly with file count, and metadata operations become the bottleneck.

---

## What OPTIMIZE Actually Does

Suppose:

```text
Partition
│
├─ file1.parquet 10MB
├─ file2.parquet 12MB
├─ file3.parquet 8MB
├─ file4.parquet 15MB
├─ file5.parquet 11MB
```

Running:

```sql
OPTIMIZE sales
```

Delta:

### Step 1

Reads file metadata from Delta Log.

```text
Which files exist?
Which are active?
Which are deleted?
```

### Step 2

Chooses candidate files.

Usually:

```text
Small files
Recently modified files
```

### Step 3

Reads those files.

### Step 4

Rewrites them into larger files.

```text
Before

10MB
12MB
8MB
15MB
11MB

After

56MB
```

### Step 5

Updates Delta Log.

Old files become:

```text
Removed
```

New file becomes:

```text
Added
```

The original files remain in storage until VACUUM removes them.

---

## Delta Log Perspective

Before:

```text
_delta_log

ADD file1
ADD file2
ADD file3
ADD file4
ADD file5
```

After OPTIMIZE:

```text
REMOVE file1
REMOVE file2
REMOVE file3
REMOVE file4
REMOVE file5

ADD optimized_file
```

This is why OPTIMIZE is ACID-safe.

Readers continue reading old versions while optimization runs.

---

## How Delta Chooses File Sizes

This is where architects start paying attention.

A common target is around:

```text
256 MB - 1 GB
```

depending on workload and platform. Databricks documentation notes that file sizes are tuned automatically in many cases and configurable for OPTIMIZE operations. ([docs.databricks.com](https://docs.databricks.com/aws/en/delta/tune-file-size?utm_source=chatgpt.com "Control data file size | Databricks on AWS"))

Think:

| File Size | Effect |
|---|---|
| 10 MB | Too many files |
| 100 MB | Better |
| 512 MB | Usually good |
| 1 GB | Common upper target |
| 5 GB | Too large |

---

## Why Not One Huge File?

Many beginners think:

```text
1 TB Table
    ↓
1 TB File
```

Bad idea. Spark parallelism disappears.

You want:

```text
1 TB Table
    ↓
1000 × 1GB files
```

Now:

```text
1000 Spark tasks
```

can run in parallel.

---

## What Happens With Z-ORDER

Now things become interesting.

Without Z-ORDER:

```sql
OPTIMIZE sales
```

Delta only compacts.

```text
Small Files
      ↓
Large Files
```

No intelligent data arrangement.

With:

```sql
OPTIMIZE sales
ZORDER BY(customer_id)
```

Delta does much more.

### Step 1

Read all candidate records.

```text
1
9000
50
7000
22
```

### Step 2

Calculate Z-values.

Conceptually:

```text
CustomerID
     ↓
Z-Curve Value
```

### Step 3

Sort by Z-value.

### Step 4

Create new files.

```text
File1
1-1000

File2
1001-2000

File3
2001-3000
```

Data with similar values gets colocated. This maximizes the effectiveness of data skipping. ([Conduktor](https://conduktor.io/glossary/optimizing-delta-tables-optimize-and-z-order?utm_source=chatgpt.com "Optimizing Delta Tables: OPTIMIZE and Z-ORDER"))

---

## Why Query Speed Improves

Suppose:

```sql
SELECT *
FROM sales
WHERE customer_id = 2500
```

After Z-Order:

```text
File1
Min=1
Max=1000

File2
Min=1001
Max=2000

File3
Min=2001
Max=3000
```

Spark immediately skips:

```text
File1
File2
```

Reads only:

```text
File3
```

This is data skipping.

---

## The Hidden Magic

Many engineers think:

```text
Z-Order speeds queries
```

Not exactly.

The real chain is:

```text
Z-Order
    ↓
Better Data Locality
    ↓
Better Min/Max Statistics
    ↓
More File Skipping
    ↓
Less I/O
    ↓
Faster Queries
```

→ **Risk:** Z-ORDER without understanding the chain leads to wrong column choices and disappointing results. Don't Z-Order low-cardinality columns.

---

## Multi-Column Z-Order

Example:

```sql
OPTIMIZE sales
ZORDER BY(
    customer_id,
    product_id,
    region
)
```

Delta attempts to keep records with similar combinations close together using a Morton/Z-curve approach. Effectiveness drops as more columns are added, so choosing columns carefully matters. ([docs.databricks.com](https://docs.databricks.com/aws/en/delta/data-skipping?utm_source=chatgpt.com "Data skipping | Databricks on AWS"))

### Tips

- Limit to 2–3 columns
- Put equality-filter columns first (not range columns)
- Don't Z-Order partition columns (they're already colocated)

---

## Architect Rules of Thumb

### Good Partition Columns

```text
event_date
year
month
region
country
```

Low-to-medium cardinality.

### Good Z-Order Columns

```text
customer_id
device_id
account_id
product_id
```

High-cardinality columns frequently used in filters.

### Bad Z-Order Columns

```text
status
Y/N
active_flag
gender
```

Very low cardinality.

Almost no benefit.

### Bad Partition Columns

```text
customer_id
email
transaction_id
```

Millions of folders.

Metadata nightmare.

---

## OPTIMIZE Is Not Free

OPTIMIZE performs a full rewrite of the selected data. Understand the costs:

| Cost | Detail |
|---|---|
| **Compute** | Reads + rewrites all candidate files. A 1 TB table with 50% small files = 500 GB rewritten |
| **Write amplification** | Data is rewritten. Storage I/O doubles temporarily |
| **Storage (temporary)** | Old files remain until VACUUM. Storage spikes during OPTIMIZE |
| **Delta Log** | New transaction log entry. Safe but adds metadata |
| **Bin-packing** | Different from Z-ORDER — just merges files without sorting. Cheaper |

### When to Run OPTIMIZE

- After high-volume streaming ingestion (hourly/daily)
- When file count exceeds ~100 per partition
- When average file size drops below ~128 MB
- Before critical reporting windows

### When to Skip OPTIMIZE

- Tables < 1 GB total
- Tables already well-partitioned with large files
- During peak query hours (OPTIMIZE generates heavy I/O)
- When bin-packing alone is sufficient (no Z-ORDER needed)

### Auto Compaction vs Manual OPTIMIZE

Databricks auto compaction helps but is not a full replacement for scheduled OPTIMIZE on large tables. ([docs.databricks.com](https://docs.databricks.com/aws/en/delta/tune-file-size?utm_source=chatgpt.com "Control data file size | Databricks on AWS"))

- **Auto Compaction:** Best-effort, triggered after writes. Good for small-to-medium tables
- **Manual OPTIMIZE:** Scheduled, predictable, can include Z-ORDER. Required for large tables

→ **Risk:** Relying solely on auto compaction for large streaming tables leads to small-file accumulation between auto-compaction cycles.

---

## Liquid Clustering

Databricks' successor to Z-ORDER — addresses key limitations:

- **No full rewrite needed** — Liquid clustering incrementally improves data layout
- **Dynamic reclustering** — new data is automatically placed correctly
- **Multiple dimensions** — no degradation with more columns

```sql
CREATE TABLE sales
USING DELTA
CLUSTER BY (customer_id, product_id);

-- Recluster existing data
ALTER TABLE sales CLUSTER BY (customer_id, product_id);
```

vs traditional Z-ORDER:

- Z-ORDER requires full OPTIMIZE rewrite every time
- Liquid Clustering is incremental and lower-cost
- Liquid Clustering works well for evolving access patterns (you can change cluster keys)

→ **Risk:** Z-ORDER on frequently updated tables requires constant re-optimization. Liquid Clustering eliminates this churn.

---

## Predictive Optimization

Databricks' OPTIMIZE and VACUUM can be set to auto-pilot:

```sql
SET spark.databricks.delta.optimizeWrite.enabled = true;
SET spark.databricks.delta.autoCompact.enabled = true;
```

### What It Does

- Automatically bins-packs small files after writes
- Automatically expires old snapshots via VACUUM
- Learns table patterns from usage

### When to Trust Auto-Pilot

- Homogeneous workloads (same query patterns)
- Streaming tables with predictable ingestion
- Teams without dedicated data engineers

### When to Stay Manual

- Complex Z-ORDER requirements
- Time-sensitive tables (don't want OPTIMIZE running during peak)
- Multi-tenant tables with conflicting access patterns
- Tables requiring strict compliance (audit trail of when data was rewritten)

---

## Real Production Lifecycle

A typical large Delta table might follow:

```text
Streaming Writes
       ↓
Many Small Files
       ↓
Auto Compaction (best-effort)
       ↓
Daily OPTIMIZE (bin-packing)
       ↓
Weekly Z-ORDER (or Liquid Clustering)
       ↓
VACUUM (retention 7 days default)
```

---

## Monitoring & Observability

Track these metrics over time:

| Metric | Where to Find | Alert Threshold |
|---|---|---|
| File count per partition | DESCRIBE DETAIL | > 100 |
| Average file size | DESCRIBE DETAIL | < 64 MB |
| Data skipping % | EXPLAIN / Query plan | < 50% |
| OPTIMIZE duration | Job history | > 2× baseline |
| Snapshot count | DESCRIBE HISTORY | Growing unbounded |
| Storage growth rate | Cloud storage metrics | Spikes after OPTIMIZE |

### Useful Commands

```sql
-- Table stats
DESCRIBE DETAIL my_table;

-- Recent optimize history
DESCRIBE HISTORY my_table;

-- File information
DESCRIBE EXTENDED my_table;
```

→ **Risk:** No monitoring = silent degradation. File count grows, queries slow, nobody notices until SLAs break.

---

## Staff Engineer View

When a query is slow, investigate in this order:

```text
1. Partition Strategy
2. Small File Count
3. File Size Distribution
4. Data Skipping %
5. Z-Order Columns
6. Query Filters
7. Join Strategy
```

A surprisingly common production issue is not Spark tuning at all.

It's:

```text
10 TB table
2 million tiny files
no optimize
no z-order
```

In that situation, fixing the storage layout often delivers a larger improvement than changing executor memory, cores, shuffle partitions, or cluster size.

---

## When to Use What: Decision Matrix

| Scenario | Use Z-ORDER | Use Liquid Clustering | Use Bin-Pack Only |
|---|---|---|---|
| New table, known queries | Maybe | Yes | No |
| High-churn streaming table | No (too expensive) | Yes | As supplement |
| Existing Z-ORDER table, happy | Keep | Evaluate migration | No |
| Occasional slow queries | One-time Z-ORDER | No | Yes |
| Multiple access patterns | Degrades | Handles well | No |
| Multi-engine (non-Databricks) | Limited support | Limited | Yes |

> **Note:** Liquid Clustering is Databricks-proprietary. For multi-engine environments, Z-ORDER + bin-packing remains the portable choice.

---

## Learning Path: Physical Data Layout Optimization

The complete hierarchy:

```text
Parquet
   ↓
Delta Log
   ↓
Data Skipping
   ↓
OPTIMIZE (bin-packing)
   ↓
Z-ORDER (data locality)
   ↓
Liquid Clustering (incremental reclustering)
   ↓
Hidden Partitioning (Iceberg)
```

That's the evolution of physical data layout optimization in modern lakehouses. Understanding each layer is what separates someone who runs OPTIMIZE from someone who designs table lifecycle strategy.
