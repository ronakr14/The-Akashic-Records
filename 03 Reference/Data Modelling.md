# 1. Data Modeling
Many ETL engineers can move data but struggle to organize it.
### Questions
* Why use a star schema?
* Star vs Snowflake?
* Fact vs Dimension?
* What makes a good partition key?
* Why avoid high-cardinality partitions?
Example:
```text
Fact_Order
------------
order_id
customer_id
product_id
amount
Dim_Customer
------------
customer_id
name
city
```
Interviewers often care more about this than ETL code.