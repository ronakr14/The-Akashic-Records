---
id: w369ac9798tiylvdr84nqya
title: Indexes
desc: ''
updated: 1755757567925
created: 1755757336762
---

# **Enterprise Multi-DB Index Cheat Sheet**

| Feature / Operation                | Purpose                     | Syntax / Example                                                                                                                                                                                                                | DB Notes / Enterprise Tips                                                                                |
| ---------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Create Index**                   | Improve query performance   | **PostgreSQL / SQL Server / Oracle / SQLite:** `CREATE INDEX idx_orders_user ON orders(user_id);` <br> **Snowflake:** Clustering key (approx. indexing): `CREATE TABLE orders CLUSTER BY (user_id);`                            | Enterprise: Use indexes on frequently filtered/joined columns.                                            |
| **Unique Index**                   | Enforce uniqueness          | `CREATE UNIQUE INDEX idx_orders_orderid ON orders(order_id);`                                                                                                                                                                   | Enterprise: prevents duplicates and enforces data integrity.                                              |
| **Composite / Multi-column Index** | Index on multiple columns   | `CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);`                                                                                                                                                             | Enterprise: improves multi-column query performance; order of columns matters.                            |
| **Partial / Filtered Index**       | Index a subset of rows      | PostgreSQL: `CREATE INDEX idx_recent_orders ON orders(order_date) WHERE order_date > CURRENT_DATE - INTERVAL '30 days';`                                                                                                        | Enterprise: reduces index size, improves performance for selective queries.                               |
| **Function / Expression Index**    | Index on computed column    | PostgreSQL: `CREATE INDEX idx_lower_email ON users(LOWER(email));`                                                                                                                                                              | Enterprise: optimize queries using expressions without storing extra columns.                             |
| **Drop Index**                     | Remove index                | `DROP INDEX idx_orders_user;` <br> SQL Server: `DROP INDEX orders.idx_orders_user;`                                                                                                                                             | Enterprise: drop unused indexes to reduce storage and write overhead.                                     |
| **Check Existing Indexes**         | Inspect current indexes     | PostgreSQL: `\di` <br> SQL Server: `SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID('orders');` <br> SQLite: `PRAGMA index_list('orders');` <br> Oracle: `SELECT index_name FROM user_indexes WHERE table_name='ORDERS';` | Enterprise: validate indexing strategy before query tuning.                                               |
| **Rebuild / Reorganize Index**     | Optimize index performance  | SQL Server: `ALTER INDEX ALL ON orders REBUILD;` <br> Oracle: `ALTER INDEX idx_orders_user REBUILD;`                                                                                                                            | Enterprise: rebuild fragmented indexes periodically to maintain performance.                              |
| **Clustered vs Non-clustered**     | Physical storage vs logical | SQL Server: `CREATE CLUSTERED INDEX idx_orders_pk ON orders(order_id);`                                                                                                                                                         | Enterprise: Clustered indexes physically sort table; one per table; non-clustered for additional queries. |
| **Automatic / System Indexes**     | Created by PK / constraints | Automatically created for PRIMARY KEY, UNIQUE constraints                                                                                                                                                                       | Enterprise: leverage PK and unique constraints to reduce manual index management.                         |
| **Best Practices**                 | Index strategy              | - Index frequently queried/filter/join columns <br> - Avoid over-indexing <br> - Use partial/composite indexes for efficiency <br> - Monitor index usage and drop unused ones <br> - Consider impact on INSERT/UPDATE/DELETE    | Enterprise: index strategy is critical for OLTP and OLAP workloads; balance read vs write performance.    |

---

## **Enterprise Design Notes**

* **SQLite:** Supports simple, unique, and composite indexes; no advanced features like partial indexes before 3.8.0.
* **PostgreSQL:** Full-featured indexing: B-tree, GIN, GiST, BRIN, expression, partial indexes.
* **Snowflake:** Uses clustering keys as “index-like” performance optimization; no traditional indexes.
* **Oracle:** Supports B-tree, bitmap, function-based, domain, and partitioned indexes.
* **SQL Server:** Clustered, non-clustered, filtered, and included column indexes; optimize for OLTP/OLAP workloads.
* **Best Practices:**

  * Regularly **monitor index usage** with DB stats/views.
  * **Avoid redundant indexes**; each index adds write overhead.
  * **Use composite indexes wisely**; column order affects query plan.
  * **Rebuild/reorganize** high-churn tables periodically.
  * Consider **indexing strategies per workload type**: OLTP (few, selective indexes), OLAP (covering, composite indexes).

---

## **Quick Examples**

```sql
-- PostgreSQL simple index
CREATE INDEX idx_orders_user ON orders(user_id);

-- PostgreSQL unique index
CREATE UNIQUE INDEX idx_orders_orderid ON orders(order_id);

-- PostgreSQL composite index
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);

-- PostgreSQL partial index
CREATE INDEX idx_recent_orders ON orders(order_date) WHERE order_date > CURRENT_DATE - INTERVAL '30 days';

-- SQL Server clustered index
CREATE CLUSTERED INDEX idx_orders_pk ON orders(order_id);

-- SQLite composite index
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);

-- Oracle function-based index
CREATE INDEX idx_lower_email ON users(LOWER(email));

-- Drop index
DROP INDEX idx_orders_user;
```

---

This cheat sheet **covers all essential index operations across major DBs**, highlighting **index creation, unique/composite/partial/function indexes, inspection, rebuild, and best practices**, making it **enterprise-ready for query optimization, OLTP/OLAP tuning, and schema design**.
