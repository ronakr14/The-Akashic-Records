**ELT:** Store the data first, then clean it.
## ELT Approach
1. Move everything to the new house first.
2. Organize and clean it inside the new house.
**Extract → Load → Transform**
```
Source Systems
      ↓
   Extract
      ↓
     Load
      ↓
 Data Warehouse
      ↓
  Transform
      ↓
Analytics Tables
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

# ELT
Load everything first:
Warehouse contains:
```
raw.website
raw.orders
raw.crm
raw.payments
```
Then transformations happen inside warehouse using SQL:
```sql
SELECT
    w.user_id,
    w.country,
    o.amount
FROM raw.website w
JOIN raw.orders o
ON w.user_id = o.user_id;
```
Result becomes:
```
analytics.customer_orders
```

# Why ELT Became Popular
Cloud changed everything.
Modern warehouses became extremely powerful:
* Snowflake
* Databricks
* Google BigQuery
* Amazon Redshift
Now warehouses can process terabytes or petabytes directly.
So:
```
Why transform outside?
Just load first and transform inside.
```
This created ELT.


## ELT = Warehouse Store
Everything arrives first.
Later workers sort and organize.
```
Store → Clean
```

# ELT Advantages
### Fast Ingestion
Load first.
Transform later.
### Keep Raw Data
Huge benefit.
If requirements change:
```
Re-run transformation
```
No need to pull data again.
### Better for AI and Analytics
Data scientists often need raw data.
ELT preserves it.
### Scales Easily
Warehouse compute handles transformations.
---
# ELT Disadvantages
### Higher Storage Cost
Raw + transformed data coexist.
### Governance Required
Bad data enters warehouse.
Need:
* data quality checks
* monitoring
* lineage
### Security Challenges
Sensitive data may already be stored.
Must control access carefully.