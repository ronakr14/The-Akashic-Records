## 8. How would you choose partition keys for:
* Orders table
* Customer table
* IoT sensor table
Why?

This is a very common interview question because **bad partitioning can make a system 10–100x slower**, while good partitioning enables partition pruning and efficient parallel processing.

The interviewer is looking for:

- Query patterns
    
- Data distribution
    
- Cardinality
    
- Partition pruning
    
- Avoiding small files and skew
    

A common mistake is:

> "Partition everything by customer_id."

That's usually a terrible choice.

---

# General Partitioning Principles

A good partition key should:

### 1. Match Query Patterns

Partition by columns frequently used in filters.

Example:

```sql
SELECT *
FROM orders
WHERE order_date BETWEEN '2026-01-01'
                     AND '2026-01-31';
```

Partitioning by `order_date` helps.

---

### 2. Avoid High Cardinality

Bad:

```text
customer_id
order_id
transaction_id
```

Millions of partitions.

---

### 3. Avoid Very Low Cardinality

Bad:

```text
gender
country (if only 3 countries)
status
```

Too few partitions.

---

### 4. Ensure Even Distribution

Avoid hotspots:

```text
90% of data in one partition
10% in all others
```

---

# 1. Orders Table

Typical schema:

```sql
orders
(
    order_id,
    customer_id,
    order_date,
    region,
    amount
)
```

---

## Typical Queries

```sql
WHERE order_date BETWEEN ...
```

```sql
WHERE order_date = ...
```

```sql
Daily Sales Reports
```

```sql
Monthly Revenue Reports
```

---

## Recommended Partition Key

```text
order_date
```

Example:

```text
orders/
  order_date=2026-06-01/
  order_date=2026-06-02/
```

---

## Why?

Most analytics are time-based.

Partition pruning works extremely well.

Example:

```sql
SELECT *
FROM orders
WHERE order_date='2026-06-01';
```

Instead of scanning:

```text
100 TB
```

you scan:

```text
1 day
```

only.

---

## For Very Large Tables

Use multi-level partitioning:

```text
order_date
region
```

Example:

```text
orders/
  order_date=2026-06-01/
      region=US/
      region=APAC/
      region=EMEA/
```

Benefits:

- Better parallelism
    
- Smaller scans
    

---

## What Not To Use

```text
order_id
```

because every order creates a new partition.

---

```text
customer_id
```

because cardinality is too high.

---

# 2. Customer Table

Typical schema:

```sql
customers
(
    customer_id,
    name,
    city,
    country,
    signup_date
)
```

---

## Key Observation

Customer tables are usually:

- Much smaller than fact tables
    
- Frequently joined
    
- Not often filtered by date
    

---

## Often: No Partitioning

If:

```text
10M customers
Few GBs
```

I'd choose:

```text
No partitioning
```

and rely on:

- Clustering
    
- Sorting
    
- Indexing
    
- Bucketing
    

---

## If Partitioning Is Needed

Use:

```text
country
```

or

```text
signup_year
```

depending on query patterns.

Example:

```text
customers/
   country=US/
   country=IN/
```

---

## Why Not Customer ID?

Bad:

```text
100 million customers
100 million partitions
```

Catastrophic metadata overhead.

---

## Interview Insight

Many senior engineers answer:

> Customer dimension tables often shouldn't be partitioned at all.

That's actually a strong answer.

---

# 3. IoT Sensor Table

This is where partitioning becomes critical.

Typical schema:

```sql
sensor_events
(
    sensor_id,
    event_time,
    temperature,
    pressure
)
```

---

## Characteristics

- Massive volume
    
- Time-series workload
    
- Continuous ingestion
    

Example:

```text
10 billion records/day
```

---

## Typical Queries

```sql
WHERE event_time BETWEEN ...
```

```sql
Last 24 Hours
```

```sql
Last Week
```

---

## Recommended Partition Key

```text
event_date
```

or

```text
event_hour
```

for very high volume systems.

---

Example:

```text
sensor_events/

   event_date=2026-06-01/

   event_date=2026-06-02/
```

---

## For Extremely Large Systems

Use:

```text
event_date
+
hash(sensor_id)
```

Example:

```text
event_date=2026-06-01/
    bucket=0
    bucket=1
    bucket=2
```

---

## Why?

Without hashing:

```text
event_date=2026-06-01
```

might contain:

```text
50 TB
```

in a single partition.

Hashing improves:

- Parallelism
    
- Load balancing
    
- Write throughput
    

---

# Partitioning Comparison

|Table|Recommended Partition Key|Why|
|---|---|---|
|Orders|`order_date`|Most queries are time-based, excellent partition pruning|
|Customer|Often none; otherwise `country` or `signup_year`|Smaller dimension table, avoids high-cardinality partitions|
|IoT Sensor|`event_date` or `event_hour`; optionally hash(sensor_id)|Massive time-series data, supports pruning and parallelism|

---

# What Interviewers Love to Hear

Don't choose partition keys based on the schema alone.

Choose them based on:

1. Query access patterns
    
2. Data volume
    
3. Cardinality
    
4. Data skew
    
5. Retention strategy
    

A concise interview answer would be:

> For the Orders table, I'd partition by `order_date` because most reporting and analytics are time-based. For the Customer table, I would often avoid partitioning entirely since it's typically a smaller dimension table; if needed, I'd use a low-to-medium cardinality field such as `country` or `signup_year`. For the IoT sensor table, I'd partition by `event_date` or even `event_hour` for very high-volume workloads, and potentially combine it with hash bucketing on `sensor_id` to improve parallelism and avoid oversized partitions. The goal is always to align partitioning with query patterns while avoiding excessive partition counts and data skew.