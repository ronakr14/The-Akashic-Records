ou discover that yesterday's batch produced incorrect results.
Downstream dashboards have already consumed the data.
Walk me through your incident response process.

This is a classic senior/staff-level data engineering incident question. Interviewers are evaluating whether you can manage **data correctness incidents**, not just technical debugging.

My approach would be structured around **containment → assessment → remediation → prevention**.

# 1. Acknowledge and Declare Incident

First, I would treat this as a production incident.

Questions I immediately ask:

- What data is incorrect?
    
- Which datasets are affected?
    
- When did the issue start?
    
- Which downstream consumers have already used it?
    
- Is this a financial, compliance, or customer-facing impact?
    

I would open an incident channel and notify:

- Analytics team
    
- Dashboard owners
    
- Data consumers
    
- Business stakeholders
    

The goal is to prevent further spread of bad data.

---

# 2. Contain the Blast Radius

Before debugging:

### Stop further consumption

Possible actions:

- Disable scheduled dashboard refreshes
    
- Pause downstream pipelines
    
- Mark affected tables as invalid
    
- Block exports to external systems
    

I don't want more users making decisions on corrupted data.

---

# 3. Assess Impact

I need to understand:

### Which partitions are affected?

Example:

```text
sales_fact
2026-06-03 partition corrupted
2026-06-02 and older look correct
```

### How much data is wrong?

Checks:

- Row counts
    
- Aggregates
    
- Reconciliation reports
    
- Data quality alerts
    

Questions:

```text
Are numbers missing?
Are rows duplicated?
Are metrics inflated?
```

---

# 4. Identify Root Cause

I would compare:

### Yesterday's successful run

vs

### Today's failed output

Areas I investigate:

#### Source data changes

```text
Unexpected schema change
Null values
Late-arriving data
Corrupted files
```

#### Pipeline code changes

```text
New deployment
Logic modification
Join condition change
Aggregation bug
```

#### Infrastructure changes

```text
Cluster configuration
Library upgrades
Engine version upgrades
```

#### Data quality reports

Example:

```text
Fact table row count dropped 40%
```

which immediately narrows investigation.

---

# 5. Determine Recovery Strategy

Depending on root cause:

## Option A: Re-run affected partition

Best case:

```text
Bug fixed
Reprocess partition
Publish corrected data
```

Example:

```text
Rebuild only 2026-06-03
```

---

## Option B: Restore previous snapshot

If using a lakehouse:

- Delta Lake Time Travel
    
- Apache Iceberg Snapshots
    
- Apache Hudi Timeline
    

I may roll back to a known-good version while root cause is investigated.

This minimizes business disruption.

---

## Option C: Full backfill

If corruption spans multiple days:

```text
Recompute affected date range
```

For example:

```text
2026-05-25 through 2026-06-03
```

---

# 6. Validate Before Republishing

Before releasing corrected data:

### Reconciliation

```text
Row counts
Business totals
Revenue numbers
Order counts
```

### Data Quality Checks

```text
Null %
Duplicate %
Referential integrity
Distribution checks
Freshness checks
```

### Business Validation

Sometimes engineering says:

```text
Pipeline succeeded
```

but finance says:

```text
Revenue is off by 20%
```

Business signoff matters.

---

# 7. Republish Corrected Data

After validation:

- Refresh dashboards
    
- Resume downstream jobs
    
- Notify stakeholders
    

Example:

```text
Corrected sales data has been republished.
Dashboards refreshed.
Issue resolved.
```

---

# 8. Perform Postmortem

The most important step.

Questions:

### Why wasn't this detected earlier?

Maybe:

```text
No data quality checks
No anomaly detection
No reconciliation
```

### Why did bad data reach consumers?

Maybe:

```text
Pipeline marked success despite bad output
```

### How can recurrence be prevented?

Examples:

#### Add automated DQ rules

```text
Revenue cannot vary >30% day-over-day
```

#### Add contract testing

```text
Schema validation
```

#### Add canary validation

```text
Validate before publishing
```

#### Add data observability

Tools:

- Great Expectations
    
- Soda
    
- Monte Carlo
    

---

# Example Senior-Level Answer

> First, I'd declare a data incident and stop further propagation of incorrect data by pausing downstream refreshes. Next, I'd assess the blast radius by identifying affected datasets, partitions, consumers, and business impact. I'd compare the bad run against the last known good run to isolate the root cause, whether it was source data, code changes, or infrastructure changes. Once identified, I'd either rerun affected partitions, restore a previous snapshot, or execute a backfill. Before republishing, I'd perform reconciliation and business validation checks. Finally, I'd conduct a postmortem and implement preventive controls such as automated data quality validation, anomaly detection, and observability monitoring to ensure similar incidents are caught before data reaches consumers.

That's typically the level of answer expected from a Senior, Lead, or Staff Data Engineer.