A batch pipeline has 20 steps.
Step 19 fails after processing 8 hours.
What would you do?
Expected:
* Checkpointing
* Restartability
* Intermediate storage
This question is testing whether you know how to build **fault-tolerant batch pipelines**. Re-running 8 hours of work because the 19th step failed is usually unacceptable.

## Immediate Actions

### 1. Investigate the Failure

First determine:

- Is it a transient failure?
    
    - Network timeout
        
    - Temporary database outage
        
    - Cluster issue
        
- Or a data issue?
    
    - Corrupt file
        
    - Schema change
        
    - Bad record
        

Check:

```text
Pipeline logs
Application logs
Infrastructure metrics
```

You don't want to blindly restart and hit the same error again.

---

## Design for Restartability

### 2. Resume from Step 19

A well-designed pipeline should support:

```text
Step 1  ✓
Step 2  ✓
...
Step 18 ✓
Step 19 ✗
Step 20 -
```

After fixing the issue:

```text
Restart from Step 19
```

not:

```text
Restart from Step 1
```

This requires tracking execution state.

Example metadata table:

```sql
pipeline_run_id
step_name
status
start_time
end_time
```

---

## Checkpointing

### 3. Persist Intermediate Results

Store outputs after major stages.

Instead of:

```text
Raw
 ↓
Step1
 ↓
Step2
 ↓
...
 ↓
Step19
```

Use:

```text
Raw
 ↓
Step1
 ↓
Checkpoint A
 ↓
Step2-10
 ↓
Checkpoint B
 ↓
Step11-18
 ↓
Checkpoint C
 ↓
Step19
```

If Step 19 fails:

```text
Restart from Checkpoint C
```

rather than reprocessing everything.

---

## Intermediate Storage

### 4. Materialize Expensive Computations

Write intermediate outputs to:

- Parquet
    
- Iceberg
    
- Delta Lake
    
- Temporary staging tables
    

Example:

```text
s3://pipeline/stage1/
s3://pipeline/stage2/
s3://pipeline/stage3/
```

This allows:

- Faster recovery
    
- Easier debugging
    
- Independent validation
    

---

## Idempotency

### 5. Ensure Safe Re-runs

If Step 19 runs twice:

```text
Result should remain correct
```

Avoid:

```sql
INSERT INTO target
```

which may duplicate records.

Prefer:

```sql
MERGE
UPSERT
OVERWRITE PARTITION
```

---

## Workflow Orchestration

### 6. Use Dependency-Aware Scheduling

Tools such as:

- Apache Airflow
    
- Dagster
    
- Prefect
    

track task state:

```text
SUCCESS
FAILED
SKIPPED
RETRYING
```

and can restart only failed tasks.

---

## Long-Term Improvements

If Step 19 regularly fails:

Ask:

### Why is it so late in the pipeline?

Maybe:

```text
Step 19 = data validation
```

Move validation earlier.

Or:

```text
Step 19 = huge aggregation
```

Break it into smaller stages.

Or:

```text
Single 8-hour monolithic job
```

Refactor into modular jobs.

---

## Interview Answer

> I would first diagnose whether the failure is transient or data-related. Assuming the first 18 steps completed successfully, I would avoid rerunning the entire pipeline. The pipeline should be designed with checkpointing and intermediate storage so outputs from earlier stages are persisted. I would restart from the last successful checkpoint, ensuring each step is idempotent so reruns are safe. Using workflow orchestration and execution metadata allows failed steps to be retried independently, reducing recovery time from hours to minutes.