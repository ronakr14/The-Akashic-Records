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