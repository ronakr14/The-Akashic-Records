---
id: 1ldqxjjemfngm6euidiggal
title: TCL
desc: ''
updated: 1755756708092
created: 1755756701363
---

# **Enterprise Multi-DB TCL (Transaction Control Language) Cheat Sheet**

| TCL Operation                       | Purpose                                     | Syntax                                           | DB Notes / Enterprise Tips                                                                                                                                                                            |                 |                                                                                                                             |
| ----------------------------------- | ------------------------------------------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **BEGIN / START TRANSACTION**       | Start a new transaction block               | `BEGIN;` or `START TRANSACTION;`                 | PostgreSQL, Oracle, SQL Server, Snowflake: fully supported. SQLite: transactions start implicitly unless autocommit disabled. Enterprise: wrap multi-step DML for atomicity.                          |                 |                                                                                                                             |
| **COMMIT**                          | Save all changes in the current transaction | `COMMIT;`                                        | Always commit after multi-step operations; in Snowflake, commit is implicit at end of DML unless wrapped in multi-statement transaction.                                                              |                 |                                                                                                                             |
| **ROLLBACK**                        | Undo all changes in current transaction     | `ROLLBACK;`                                      | Critical for error handling and ETL pipelines.                                                                                                                                                        |                 |                                                                                                                             |
| **SAVEPOINT**                       | Set a savepoint inside a transaction        | `SAVEPOINT savepoint_name;`                      | Allows partial rollback; supported in PostgreSQL, Oracle, SQL Server, SQLite, Snowflake (multi-statement transactions).                                                                               |                 |                                                                                                                             |
| **ROLLBACK TO SAVEPOINT**           | Undo changes up to a savepoint              | `ROLLBACK TO SAVEPOINT savepoint_name;`          | Useful for nested operations or error recovery in enterprise scripts.                                                                                                                                 |                 |                                                                                                                             |
| **RELEASE SAVEPOINT**               | Remove a savepoint without rolling back     | `RELEASE SAVEPOINT savepoint_name;`              | Frees resources; supported in PostgreSQL, Oracle, SQL Server. SQLite: supported. Snowflake: supports savepoints with multi-statement transactions.                                                    |                 |                                                                                                                             |
| **SET TRANSACTION ISOLATION LEVEL** | Define concurrency behavior                 | \`SET TRANSACTION ISOLATION LEVEL READ COMMITTED | REPEATABLE READ                                                                                                                                                                                       | SERIALIZABLE;\` | PostgreSQL, SQL Server, Oracle, Snowflake support various isolation levels. SQLite: SERIALIZABLE and READ UNCOMMITTED only. |
| **AUTOCOMMIT Control**              | Enable/disable auto-commit mode             | `SET autocommit = OFF;`                          | PostgreSQL / Snowflake: auto-commit default ON. SQL Server: transactions begin implicitly unless explicit. SQLite: auto-commit default ON. Enterprise: disable auto-commit for multi-step operations. |                 |                                                                                                                             |

---

## **Enterprise Design Notes**

* **SQLite:** Supports transactions and savepoints; autocommit mode by default. No multi-version concurrency like PostgreSQL.
* **PostgreSQL:** Full-featured; supports savepoints, nested transactions (via savepoints), and configurable isolation levels.
* **Snowflake:** Supports multi-statement transactions, savepoints, rollback; some DDL auto-commits.
* **Oracle:** Supports transactions, savepoints, rollback, isolation levels; DDL auto-commits by default.
* **SQL Server:** Supports explicit transactions, savepoints (`SAVE TRANSACTION`), isolation levels; some DDL auto-commits.
* **Best Practices:**

  * Wrap multi-step ETL/DML operations in explicit transactions.
  * Use savepoints for granular error recovery in long-running transactions.
  * Commit frequently in production to reduce lock contention.
  * Review isolation levels for concurrency-sensitive workloads.
  * Be aware that **DDL statements may auto-commit** in some DBs (Oracle, SQL Server).

---

## **Quick Examples**

```sql
-- Start transaction
BEGIN;

-- DML operations
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Savepoint for partial rollback
SAVEPOINT deduct_done;

-- Attempt risky operation
UPDATE accounts SET balance = balance / 0 WHERE id = 3;

-- Rollback to savepoint if error occurs
ROLLBACK TO SAVEPOINT deduct_done;

-- Commit transaction
COMMIT;

-- Rollback entire transaction (if needed)
ROLLBACK;

-- Set transaction isolation level (PostgreSQL / SQL Server)
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Release savepoint
RELEASE SAVEPOINT deduct_done;
```

---

This cheat sheet **covers all essential TCL operations across major DBs**, highlighting **transactions, savepoints, rollback, commit, and isolation levels**, making it **enterprise-ready for safe, controlled data manipulation in production and ETL pipelines**.

