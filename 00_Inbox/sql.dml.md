---
id: lgosofrf1n2jtns0pyt4r8m
title: Dml
desc: ''
updated: 1755880400591
created: 1755756565164
---

# **Enterprise Multi-DB DML Operations Cheat Sheet**

| DML Operation                       | Purpose   p                        | Syntax                                                                                                                                                                   | DB Notes / Enterprise Tips                                                                                                                          |
| ----------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **INSERT**                          | Add new rows                      | `INSERT INTO table_name (col1, col2) VALUES (val1, val2);`                                                                                                               | Use `RETURNING` in PostgreSQL/Oracle for inserted rows; SQLite supports `INSERT OR REPLACE` for upserts; Snowflake supports `INSERT ... RETURNING`. |
| **INSERT ... ON CONFLICT / UPSERT** | Insert or update if exists        | PostgreSQL: `INSERT ... ON CONFLICT (col) DO UPDATE SET ...;` <br> SQLite: `INSERT OR REPLACE INTO ...` <br> SQL Server: `MERGE` <br> Oracle: `MERGE INTO ... USING ...` | Enterprise: Use for idempotent operations in ETL pipelines.                                                                                         |
| **UPDATE**                          | Modify existing rows              | `UPDATE table_name SET col1 = val1 WHERE condition;`                                                                                                                     | Always use `WHERE` to prevent mass updates. Wrap in transaction for safety.                                                                         |
| **DELETE**                          | Remove rows                       | `DELETE FROM table_name WHERE condition;`                                                                                                                                | Consider soft delete (`deleted_at` column) for audit compliance.                                                                                    |
| **MERGE / UPSERT (Enterprise)**     | Combine insert/update             | SQL Server / Oracle / Snowflake: `MERGE INTO target USING source ON condition WHEN MATCHED THEN UPDATE ... WHEN NOT MATCHED THEN INSERT ...;`                            | Preferred for ETL pipelines and data synchronization.                                                                                               |
| **SELECT**                          | Query rows                        | `SELECT col1, col2 FROM table_name WHERE condition;`                                                                                                                     | Combine with joins, aggregation, window functions. Enterprise: always specify columns, avoid `SELECT *`.                                            |
| **JOINs in DML**                    | Combine data from multiple tables | PostgreSQL / Oracle / SQL Server / Snowflake: `INSERT INTO target SELECT t1.col1, t2.col2 FROM t1 JOIN t2 ON t1.id = t2.id;`                                             | SQLite: no RIGHT or FULL JOIN; consider workarounds.                                                                                                |
| **Transactions**                    | Ensure atomic operations          | `BEGIN; ... COMMIT;` / `ROLLBACK;`                                                                                                                                       | SQLite: autocommit by default. PostgreSQL, Oracle, SQL Server fully support. Snowflake: implicit transactions. Use transactions for multi-step DML. |
| **RETURNING / OUTPUT**              | Get affected rows                 | PostgreSQL/Oracle: `INSERT ... RETURNING *;` <br> SQL Server: `OUTPUT inserted.*`                                                                                        | Enterprise: useful for logging, ETL pipelines, downstream processing.                                                                               |
| **Batch Operations**                | Bulk insert/update/delete         | `INSERT INTO table SELECT ... FROM staging_table;`                                                                                                                       | Use batching for large data to reduce transaction size. Snowflake supports `COPY INTO` for bulk load from external stage.                           |

---

## **Enterprise Design Notes**

* **SQLite:** Supports basic DML; limited UPSERT (`INSERT OR REPLACE`); transactions supported but table-level locks may block concurrency.
* **PostgreSQL:** Full-featured; supports UPSERT, RETURNING, transactions, CTEs, window functions.
* **Snowflake:** Cloud-native; supports MERGE, transactions, bulk load with `COPY INTO`; constraints are metadata-only.
* **Oracle:** Enterprise-grade; supports MERGE, RETURNING INTO, multi-table updates via CTE, transactions with savepoints.
* **SQL Server:** Full DML support; MERGE for UPSERT; OUTPUT clause for affected rows; transactional safety supported.
* **Best Practices:**

  * Always wrap multi-step DML in transactions.
  * Prefer UPSERT/MERGE for idempotent ETL operations.
  * Use RETURNING / OUTPUT for audit and downstream processing.
  * Avoid `SELECT *` in DML; specify columns for maintainability and performance.

---

## **Quick Examples**

```sql
-- Insert
INSERT INTO users (id, username, email) VALUES (1, 'alice', 'alice@example.com');

-- Insert with UPSERT (PostgreSQL)
INSERT INTO users(id, username)
VALUES (1, 'alice')
ON CONFLICT(id) DO UPDATE SET username = EXCLUDED.username;

-- Update
UPDATE users SET status='active' WHERE id=1;

-- Delete
DELETE FROM users WHERE id=1;

-- Merge / UPSERT (SQL Server / Oracle)
MERGE INTO users AS target
USING staging_users AS source
ON target.id = source.id
WHEN MATCHED THEN UPDATE SET target.username = source.username
WHEN NOT MATCHED THEN INSERT (id, username) VALUES (source.id, source.username);

-- Transaction
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id=1;
UPDATE accounts SET balance = balance + 100 WHERE id=2;
COMMIT;

-- Select with join
INSERT INTO reporting.users_info (id, email, total_orders)
SELECT u.id, u.email, COUNT(o.id)
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.email;
```

---

This cheat sheet **covers all essential DML operations across major DBs**, highlighting **differences in UPSERT, MERGE, RETURNING/OUTPUT, transactions, and batch operations**, making it **enterprise-ready for ETL, reporting, and transactional workloads**.

