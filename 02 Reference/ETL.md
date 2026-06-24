---
type: concept
---

#etl #dataengineering #datawarehouse #transformation #airflow #dbt #informatica

```table-of-contents
```

**ETL:** Clean the data first, then store it.
## ETL Approach
1. Clean and organize everything **before** loading the truck.
2. Put only the cleaned items into the new house.
**Extract → Transform → Load**
```
Source Systems
      ↓
   Extract
      ↓
  Transform
(clean, join, aggregate)
      ↓
     Load
      ↓
 Data Warehouse
```

# Let's Use a Real Example
Suppose you run an ecommerce company.
Data comes from:
* Website
* Mobile App
* Payment Gateway
* CRM
* Marketing Platform
## Raw Data
Website:

| user_id | country |
| ------- | ------- |
| 1       | India   |
| 2       | USA     |
Orders:

| user_id | amount |
| ------- | ------ |
| 1       | 1000   |
| 2       | 2000   |

---
# ETL
Before loading:
### Transform Step
Join tables:

| user_id | country | amount |
| ------- | ------- | ------ |
| 1       | India   | 1000   |
| 2       | USA     | 2000   |
Remove duplicates.
Convert currencies.
Apply business rules.
Then load only final result into warehouse.


# Why ETL Existed
Years ago:
* Databases were expensive
* Storage was expensive
* Compute was limited
Warehouses couldn't handle huge transformations.
So engineers transformed data elsewhere.
Common ETL tools:
* Informatica PowerCenter
* IBM DataStage
* Microsoft SSIS
Workflow:
```
Source
  ↓
ETL Server
  ↓
Warehouse
```
The ETL server did all heavy lifting.

# Simple Analogy
## ETL = Restaurant Kitchen
Chef cleans vegetables before putting them into storage.
```
Clean → Store
```

# ETL Advantages
### Better Data Quality Before Storage
Bad data never enters warehouse.
### Lower Storage Usage
Only processed data is stored.
### Useful for Compliance
Sensitive fields can be removed before loading.
Example:
```
Credit Card Number
```
can be masked before warehouse.
---
# ETL Disadvantages
### Slow
Must transform before loading.
### Less Flexible
If business asks new questions:
```
Need new transformation
Need pipeline change
Need reload
```
### Scaling Issues
ETL servers become bottlenecks.

---

# ETL in Practice — Concrete Example

Simple Python ETL script (pandas):

```python
import pandas as pd

# Extract
orders = pd.read_csv("orders_raw.csv")
users = pd.read_sql("SELECT * FROM users", connection)

# Transform
df = orders.merge(users, on="user_id")
df = df.drop_duplicates()
df["amount_inr"] = df["amount_usd"] * 83.5
df = df[df["amount_inr"] > 0]  # remove invalid

# Load
df.to_sql("clean_orders", connection, if_exists="append", index=False)
```

Orchestrated via **Apache Airflow** DAG:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG("etl_pipeline", schedule="@daily") as dag:
    extract = PythonOperator(task_id="extract", python_callable=extract_data)
    transform = PythonOperator(task_id="transform", python_callable=transform_data)
    load = PythonOperator(task_id="load", python_callable=load_data)

    extract >> transform >> load
```

---

# ETL in 2024+

The definition of ETL has expanded:

| Era | Approach | Tools |
|---|---|---|
| 1990s–2000s | Traditional ETL | Informatica, DataStage, SSIS |
| 2010s | ELT emerges | dbt, Airbyte, Fivetran + cloud warehouses |
| 2020s | Streaming ETL | Kafka + Flink, Spark Structured Streaming |
| 2024+ | Data engineering platforms | dbt (transform), Airbyte/Fivetran (ingest), Airflow (orchestrate), Monte Carlo (observability) |

Key shift: the "T" (Transform) now happens *inside* the warehouse via SQL (dbt), not on a separate ETL server.

---

# Quick Decision Signals

| Signal | Use ETL | Use ELT |
|---|---|---|
| Sensitive data (PII, PCI) | Mask before loading | — |
| Legacy source systems | Transform at edge | — |
| Cloud warehouse available | — | Load raw, transform in-warehouse |
| Need raw data for ML | — | Load raw first |
| Regulatory compliance | Pre-load validation | — |

For full comparison, see [[ETL vs ELT]].

---

## Related Notes

- [[ETL vs ELT]] — comparison and when to use which
- [[Data Lake]] — where raw data lands before transformation
- [[Batch Processing]] — scheduling and orchestration patterns
- [[Incremental Load Strategy]] — CDC and delta loading techniques
- [[Idempotency]] — ensuring safe re-runs of ETL pipelines