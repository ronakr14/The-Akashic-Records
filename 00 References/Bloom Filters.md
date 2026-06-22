Bloom Filters are one of those concepts that seem simple at first, but they're everywhere in modern data systems.

Think of a Bloom Filter as:

> A very small, memory-efficient structure that can quickly tell you if something is **definitely not present** or **possibly present**.

Notice the wording:

```text
Definitely Not Present  ✅
Possibly Present        ✅
Definitely Present      ❌
```

That's the key tradeoff.

---

# Real-Life Analogy

Imagine a nightclub.

The bouncer has:

- A complete guest list (large)
    
- A small cheat sheet (Bloom Filter)
    

You ask:

```text
Is Ronak on the list?
```

The cheat sheet says:

```text
No
```

Then Ronak is definitely not on the guest list.

But if it says:

```text
Maybe
```

The bouncer still needs to check the actual guest list.

---

# Why Not Just Use a HashSet?

A HashSet gives:

```python
if value in set:
```

Very accurate.

But imagine:

```text
10 Billion Customer IDs
```

HashSet memory:

```text
Hundreds of GB
```

Bloom Filter:

```text
Few GB
```

Huge savings.

---

# Internal Working

Suppose we want to store:

```text
Alice
Bob
Charlie
```

Create a bit array:

```text
0 0 0 0 0 0 0 0 0 0
```

Use 3 hash functions.

---

## Insert "Alice"

Hashes produce:

```text
2
5
8
```

Set bits:

```text
0 0 1 0 0 1 0 0 1 0
```

---

## Insert "Bob"

Hashes produce:

```text
1
5
9
```

Set bits:

```text
0 1 1 0 0 1 0 0 1 1
```

---

## Query "David"

Hashes produce:

```text
3
5
8
```

Check bits:

```text
bit 3 = 0
```

Immediately:

```text
David NOT present
```

No need to check further.

---

## Query Another Value

Hashes produce:

```text
1
5
8
```

All bits are set:

```text
1
1
1
```

Result:

```text
Maybe Present
```

Could be real.

Could be coincidence.

This is called a:

```text
False Positive
```

---

# False Positives

Bloom Filters can say:

```text
Yes, maybe present
```

when actually:

```text
Not present
```

But they can NEVER say:

```text
Not present
```

for something that is actually stored.

That's why they're safe for filtering.

---

# Why Data Engineers Care

Imagine a Parquet file with:

```text
1 Billion rows
```

Query:

```sql
SELECT *
FROM orders
WHERE customer_id = 12345
```

Without Bloom Filter:

```text
Read many row groups
Check statistics
Read data
```

With Bloom Filter:

```text
Row Group 1 -> definitely not
Row Group 2 -> definitely not
Row Group 3 -> maybe
```

Read only Row Group 3.

Huge I/O reduction.

---

# Bloom Filters vs Min/Max Statistics

You learned earlier that Parquet stores:

```text
Min = 100
Max = 500
```

Suppose query:

```sql
WHERE id = 250
```

Need to read because:

```text
250 is between 100 and 500
```

Statistics can't help.

---

Bloom Filter can:

```text
250 definitely absent
```

Then skip entire row group.

This is why Bloom Filters complement statistics.

---

# In Parquet

Row Group Metadata:

```text
Row Group
    ├─ Min/Max
    ├─ Null Count
    ├─ Bloom Filter
```

Query Engine:

```text
Footer Read
    ↓
Statistics Check
    ↓
Bloom Filter Check
    ↓
Read Data
```

More pruning.

Less scanning.

---

# Where Else Are Bloom Filters Used?

### Databases

- Apache Cassandra
    
- Apache HBase
    
- PostgreSQL (certain execution plans)
    
- Apache Spark
    

---

### Data Lakes

- Apache Iceberg
    
- Delta Lake
    
- Parquet
    

---

### Caching Systems

Before querying backend:

```text
Is key present?
```

Bloom Filter avoids unnecessary lookups.

---

### Web Companies

- Google
    
- Meta
    
- LinkedIn
    

use Bloom Filters extensively for distributed storage systems.

---

# Architect Perspective

When data grows to:

```text
TBs
PBs
```

CPU is usually not the bottleneck.

The bottleneck becomes:

```text
Disk I/O
Network I/O
```

Bloom Filters exist to answer:

> "Can I avoid reading this data entirely?"

A good architect treats Bloom Filters as a **data skipping mechanism**, not a search mechanism.

Think of the optimization hierarchy:

```text
Partition Pruning
        ↓
File Pruning
        ↓
Min/Max Statistics
        ↓
Bloom Filters
        ↓
Actual Scan
```

This stack is what makes modern lakehouses fast even when datasets reach petabyte scale.

The next interesting topic would be how **Parquet Row Groups + Bloom Filters + Delta Lake data skipping + Z-Ordering** work together. That's where the performance engineering side of lakehouse architecture gets really interesting.