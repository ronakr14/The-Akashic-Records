Since you're already thinking like a Data Engineer and aiming toward Architect-level understanding, I'll explain Parquet from the storage-engine perspective rather than the usual "it's a columnar file format" definition.

# Why Parquet Exists

Imagine a table:

|CustomerID|Name|City|Salary|
|---|---|---|---|
|1|John|London|50000|
|2|Alice|Paris|60000|
|3|Bob|London|55000|

Traditional CSV stores data row by row:

```text
1,John,London,50000
2,Alice,Paris,60000
3,Bob,London,55000
```

If your query is:

```sql
SELECT AVG(Salary)
FROM customers
```

CSV must read all columns.

Parquet only reads:

```text
Salary Column
50000
60000
55000
```

This is why Parquet became the standard for Data Lakes.

---

# Architect View

Think of Parquet as:

```text
Dataset
    ↓
Parquet Files
    ↓
Row Groups
    ↓
Column Chunks
    ↓
Pages
```

Let's unpack this.

---

# Level 1: Parquet File Structure

A Parquet file looks like:

```text
+----------------+
| File Header    |
+----------------+
| Row Group 1    |
+----------------+
| Row Group 2    |
+----------------+
| Row Group 3    |
+----------------+
| Metadata       |
+----------------+
| PAR1           |
+----------------+
```

The metadata is stored at the end.

Why?

Because writers don't know final statistics until writing completes.

At the end Parquet writes:

```text
Column Names
Data Types
Compression
Statistics
Offsets
Encoding
```

Readers first jump to footer.

This is called:

```text
Footer Metadata Architecture
```

Very important interview topic.

---

# Level 2: Row Groups

Suppose file contains:

```text
100 million rows
```

Parquet doesn't store one giant block.

Instead:

```text
File
 ├─ Row Group 1 (10M rows)
 ├─ Row Group 2 (10M rows)
 ├─ Row Group 3 (10M rows)
 ...
```

Each row group is independently readable.

Benefits:

- Parallel processing
    
- Predicate pushdown
    
- Better distribution
    

Spark executors can process row groups independently.

Think:

```text
Row Group = Unit of Parallelism
```

---

# Level 3: Column Chunks

Inside each row group:

```text
Row Group
    ├─ CustomerID Column Chunk
    ├─ Name Column Chunk
    ├─ City Column Chunk
    └─ Salary Column Chunk
```

Instead of:

```text
1 John London 50000
2 Alice Paris 60000
```

It becomes:

```text
CustomerID:
1
2

Name:
John
Alice

City:
London
Paris

Salary:
50000
60000
```

This is why analytical queries become fast.

---

# Level 4: Pages

Column chunks are further divided:

```text
Salary Chunk
    ├─ Page 1
    ├─ Page 2
    ├─ Page 3
```

Page is smallest unit Parquet reads.

Typical page sizes:

```text
8 KB
16 KB
64 KB
```

depending on configuration.

---

# Internal Hierarchy

```text
Parquet File
│
├── Row Group
│     │
│     ├── Column Chunk
│     │       │
│     │       ├── Page
│     │       ├── Page
│     │       └── Page
│     │
│     └── Column Chunk
│
└── Footer Metadata
```

This diagram alone explains 70% of Parquet internals.

---

# Compression Magic

CSV:

```text
London
London
London
London
London
```

Parquet sees repetition.

It applies:

### Dictionary Encoding

Store:

```text
Dictionary

0 -> London
1 -> Paris
```

Actual data:

```text
0
0
0
1
0
```

Huge reduction.

---

Then Compression

Parquet supports:

- Snappy
    
- Gzip
    
- Brotli
    
- LZO
    
- ZSTD
    

Most common today:

```text
Snappy
```

Best balance of:

```text
Compression
+
Read Speed
```

---

# Statistics Stored in Footer

For each column:

```text
Salary

Min = 50000
Max = 70000
Nulls = 100
```

Stored per row group.

Example:

```sql
SELECT *
FROM employee
WHERE salary > 100000
```

Row Group Stats:

```text
RG1
Min=10000
Max=50000

RG2
Min=60000
Max=90000

RG3
Min=110000
Max=150000
```

Spark immediately skips:

```text
RG1
RG2
```

Reads only:

```text
RG3
```

This is called:

```text
Predicate Pushdown
```

One of the biggest performance wins.

---

# Why Spark Loves Parquet

Query:

```sql
SELECT salary
FROM employee
WHERE city='London'
```

Spark performs:

```text
1. Read footer
2. Check statistics
3. Skip irrelevant row groups
4. Read only City and Salary columns
5. Ignore all others
```

Result:

```text
Less I/O
Less Network
Less CPU
```

---

# Nested Data Support

Parquet handles:

```json
{
  "customer": {
    "name": "John",
    "address": {
      "city": "London"
    }
  }
}
```

using:

```text
Definition Levels
Repetition Levels
```

This is one of the most complex parts of Parquet internals.

That's how Parquet efficiently stores:

- Structs
    
- Arrays
    
- Maps
    
- Nested JSON
    

without flattening everything.

---

# What Happens During a Spark Read?

```text
spark.read.parquet()
        │
        ▼
Read Footer
        │
        ▼
Schema Discovery
        │
        ▼
Predicate Pushdown
        │
        ▼
Column Pruning
        │
        ▼
Row Group Selection
        │
        ▼
Page Reads
        │
        ▼
DataFrame
```

This pipeline is worth understanding deeply because it explains many Spark optimization behaviors.

---

# Architect-Level Mental Model

Think of Parquet as a mini database inside a file.

A Parquet file contains:

```text
Data
+
Schema
+
Indexes (statistics)
+
Compression
+
Column Storage
```

which means:

```text
CSV  = Raw Data
Parquet = Smart Data
```

That's why modern platforms such as Apache Spark, Databricks, Snowflake, Apache Iceberg, and Delta Lake all use Parquet as their underlying storage format.

The next step beyond Parquet itself is understanding:

1. Row Groups sizing (128 MB vs 512 MB vs 1 GB)
    
2. Predicate Pushdown internals
    
3. Dictionary Encoding vs Run-Length Encoding
    
4. Bloom Filters in Parquet
    
5. How Delta Lake and Iceberg build transaction layers on top of Parquet
    
6. Small-file problem and file compaction
    

Those topics are where Data Engineer knowledge starts transitioning into Architect-level lakehouse design.