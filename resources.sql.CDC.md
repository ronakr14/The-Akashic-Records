---
id: hthhlh97h0ugfoleueu6e8r
title: CDC
desc: ''
updated: 1755757211837
created: 1755757204023
---

# **Enterprise Multi-DB CDC (Change Data Capture) Cheat Sheet**

| Feature / Operation           | Purpose                                                               | Syntax / Example                                                                                                                                                                                                                                                             | DB Notes / Enterprise Tips                                                                                           |
| ----------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **CDC Overview**              | Track changes (INSERT, UPDATE, DELETE) for ETL, replication, auditing | N/A                                                                                                                                                                                                                                                                          | Enterprise: CDC enables near real-time data pipelines, auditing, and incremental ETL without full table scans.       |
| **Supported Methods**         | How CDC is implemented                                                | - **Log-based:** Reads DB transaction logs (PostgreSQL, Oracle, SQL Server, Snowflake Streams) <br> - **Trigger-based:** Uses triggers on tables (SQLite, PostgreSQL, Oracle, SQL Server) <br> - **Timestamp-based / column-based:** Tracks changes via last\_updated column | Enterprise: log-based is more efficient for high-volume tables; trigger-based is simpler but may impact performance. |
| **SQL Server CDC**            | Built-in CDC feature                                                  | \`\`\`sql                                                                                                                                                                                                                                                                    |                                                                                                                      |
| -- Enable CDC on DB           |                                                                       |                                                                                                                                                                                                                                                                              |                                                                                                                      |
| EXEC sys.sp\_cdc\_enable\_db; |                                                                       |                                                                                                                                                                                                                                                                              |                                                                                                                      |

\-- Enable CDC on table
EXEC sys.sp\_cdc\_enable\_table
@source\_schema = 'dbo',
@source\_name = 'orders',
@role\_name = NULL;
\-- Query changes
SELECT \* FROM cdc.dbo\_orders\_CT;

````| Enterprise: monitors table changes, captures metadata (operation, timestamp, etc.). |
| **PostgreSQL Logical Replication / WAL-based CDC** | Track changes via Write-Ahead Log | Use `pgoutput` plugin or Debezium / Kafka Connect for CDC | Enterprise: efficient for high-volume tables; can replicate to other DBs or streaming platforms. |
| **Oracle CDC** | LogMiner / GoldenGate | ```sql
-- Using Oracle GoldenGate for CDC
-- Configure capture process on table
``` | Enterprise: log-based CDC is robust for high-volume production systems. |
| **Snowflake Streams** | Track table changes for CDC | ```sql
CREATE STREAM orders_stream ON TABLE orders; 
SELECT * FROM orders_stream;``` | Enterprise: streams store inserts, updates, deletes; combine with tasks for automated ETL. |
| **SQLite Trigger-based CDC** | Track changes via triggers | ```sql
CREATE TABLE orders_audit AS SELECT * FROM orders WHERE 0;
CREATE TRIGGER orders_insert AFTER INSERT ON orders
BEGIN
    INSERT INTO orders_audit VALUES (NEW.*);
END;``` | Lightweight for small/embedded DBs. Not suitable for high-volume enterprise CDC. |
| **Best Practices** | Optimize CDC for enterprise | - Prefer log-based for high volume <br> - Track change metadata (operation type, timestamp, user) <br> - Ensure retention policies for CDC tables/streams <br> - Test CDC lag and consistency <br> - Integrate with ETL pipelines (Kafka, Debezium, Airflow) | Enterprise-grade CDC ensures minimal latency and accurate incremental data capture. |
| **Integration** | Use captured data in pipelines | ETL tools, data warehouses, streaming platforms (Kafka, Spark, Snowflake, Redshift) | Enterprise: allows incremental processing instead of full table scans, reducing cost and time. |

---

## **Enterprise Design Notes**
- **SQLite:** No built-in CDC; use triggers or application-level tracking.  
- **PostgreSQL:** Logical replication or WAL-based CDC for high-volume incremental updates; triggers for small tables.  
- **Snowflake:** Streams + tasks provide near real-time CDC; handles inserts, updates, deletes.  
- **Oracle:** LogMiner or GoldenGate for enterprise-grade log-based CDC; supports cross-DB replication.  
- **SQL Server:** Built-in CDC with system tables; easy to enable per table or database; integrates with ETL pipelines.  
- **Best Practices:**  
  - Always include **change metadata**: operation type, timestamp, user, transaction ID.  
  - Monitor **latency and throughput** for real-time pipelines.  
  - Use **incremental loads** in data warehouses to optimize performance.  
  - Retain CDC logs/streams as per enterprise retention and compliance policies.  

---

## **Quick Examples**

```sql
-- SQL Server CDC: enable CDC on DB & table
EXEC sys.sp_cdc_enable_db;
EXEC sys.sp_cdc_enable_table @source_schema='dbo', @source_name='orders', @role_name=NULL;
SELECT * FROM cdc.dbo_orders_CT;

-- Snowflake CDC using streams
CREATE STREAM orders_stream ON TABLE orders;
SELECT * FROM orders_stream;

-- SQLite trigger-based CDC (small scale)
CREATE TABLE orders_audit AS SELECT * FROM orders WHERE 0;
CREATE TRIGGER orders_insert AFTER INSERT ON orders
BEGIN
    INSERT INTO orders_audit VALUES (NEW.*);
END;
````

---

This cheat sheet **covers all essential CDC operations across major DBs**, highlighting **log-based, trigger-based, stream-based CDC, setup, integration, and best practices**, making it **enterprise-ready for real-time ETL, analytics, and audit pipelines**.
