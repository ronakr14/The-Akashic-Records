Explain the difference between:
* Retry
* Resume
* Restart
* Reprocess
This is a deceptively simple interview question. Many candidates treat these terms as synonyms, but in production batch systems they mean **very different recovery strategies**.

Think of them as increasing levels of work performed after a failure.

|Term|What Happens?|Data Re-read?|Cost|
|---|---|---|---|
|Retry|Run the same failed task again|No|Lowest|
|Resume|Continue from last checkpoint|Partial|Low|
|Restart|Start the job from the beginning|Yes|Medium|
|Reprocess|Recompute data that was already successfully processed|Yes|Highest|

---

# 1. Retry

### Definition

Attempt the same operation again after a transient failure.

Example:

```text
Step 1: Extract
Step 2: Load ← failed due to network timeout
```

System:

```text
Retry Load
```

without re-running extraction.

---

## Typical Causes

- Network timeout
    
- Temporary database outage
    
- API rate limiting
    
- Object storage transient error
    

---

## Example

```text
Load file A
      ↓
Connection lost
      ↓
Retry
      ↓
Success
```

---

## Characteristics

- Fastest recovery
    
- Usually automatic
    
- Same input
    
- Same execution step
    

---

## Interview Sound Bite

> Retry is used for transient failures where rerunning the same operation is expected to succeed without changing inputs or state.

---

# 2. Resume

### Definition

Continue processing from the last successful checkpoint.

Example:

```text
100 partitions

1-60 completed
61 failed
```

Resume from:

```text
Partition 61
```

instead of:

```text
Partition 1
```

---

## Example

```text
Day01 ✔
Day02 ✔
Day03 ✔
Day04 ✖
```

Resume:

```text
Day04
```

---

## Requires

Checkpoint metadata:

```sql
job_id
partition
status
```

Example:

|Partition|Status|
|---|---|
|Jan|Complete|
|Feb|Complete|
|Mar|Failed|

---

## Characteristics

- Efficient
    
- Avoids duplicate work
    
- Common in Spark and Airflow workflows
    

---

## Interview Sound Bite

> Resume continues execution from the last successful checkpoint rather than repeating already completed work.

---

# 3. Restart

### Definition

Run the entire job from the beginning.

Example:

```text
Process 100 partitions
```

Failure at:

```text
Partition 99
```

Restart:

```text
Partition 1
```

again.

---

## Example

```text
Extract
Transform
Load
```

Failure during load:

```text
Restart Entire Pipeline
```

---

## Why Restart?

Sometimes:

- No checkpoints exist
    
- State is corrupted
    
- Simpler than recovery
    

---

## Drawback

Very expensive.

Example:

```text
12-hour job
Fails at hour 11
```

Restart means:

```text
Run another 12 hours
```

---

## Interview Sound Bite

> Restart discards previous progress and executes the entire workflow from the beginning.

---

# 4. Reprocess

### Definition

Intentionally run data through the pipeline again, even though it was previously processed successfully.

This is not necessarily failure recovery.

---

## Common Reasons

### Business Logic Changed

Example:

```text
Tax calculation bug fixed
```

Need:

```text
Jan → Mar data recalculated
```

---

### New Transformation

Example:

```text
Added customer segmentation
```

Need historical results.

---

### Data Corrections

Example:

```text
Source system fixed records
```

Need updated outputs.

---

## Example

```text
Raw Data
     ↓
Old Logic
     ↓
Gold Table
```

New requirement:

```text
Raw Data
     ↓
New Logic
     ↓
Rebuild Gold Table
```

---

## Characteristics

- Reads historical data
    
- Produces new outputs
    
- Usually expensive
    
- Often done as a backfill
    

---

## Interview Sound Bite

> Reprocessing reruns historical data through the pipeline, usually because business rules, source data, or transformation logic have changed.

---

# Real Example

Imagine a sales pipeline.

```text
Daily Sales ETL
```

### Scenario 1

Database connection dropped.

Action:

```text
Retry
```

---

### Scenario 2

Processed:

```text
Jan
Feb
Mar
```

Failed on:

```text
Apr
```

Action:

```text
Resume from Apr
```

---

### Scenario 3

No checkpoints available.

Failed on:

```text
Apr
```

Action:

```text
Restart entire ETL
```

---

### Scenario 4

Revenue formula was wrong for last year.

Action:

```text
Reprocess last year
```

---

# How Senior Data Platforms Handle This

A mature batch platform supports all four:

```text
Retry
   ↓
Resume
   ↓
Restart
   ↓
Reprocess
```

in that order of preference.

Why?

Because cost increases dramatically as you move down the list.

---

# Interview Summary Answer

> Retry, resume, restart, and reprocess are different recovery strategies. Retry reruns a failed operation without changing inputs and is typically used for transient failures. Resume continues execution from the last successful checkpoint, avoiding already completed work. Restart reruns the entire job from the beginning when checkpoints are unavailable or state is inconsistent. Reprocess is different because it intentionally reruns historical data that may have already been processed successfully, usually due to logic changes, source corrections, or backfill requirements. In production systems, I prefer checkpoint-based resume whenever possible because it minimizes recovery time and compute costs.