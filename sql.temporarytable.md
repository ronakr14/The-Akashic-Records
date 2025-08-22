---
id: ldge2ri8apdm3b328cjz44g
title: Temporarytable
desc: ''
updated: 1755757780804
created: 1755757774714
---

# **Enterprise Multi-DB Temp Tables & Variables Cheat Sheet**

| Feature / Operation                            | Purpose                                             | Syntax / Example                                                                                                                                                                                                                                                                                                                                                                                                                    | DB Notes / Enterprise Tips                                                                                |
| ---------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Temporary Table**                            | Store intermediate results for session or procedure | **PostgreSQL:** `CREATE TEMP TABLE temp_orders (id INT, amount NUMERIC);` <br> **SQLite:** `CREATE TEMP TABLE temp_orders (id INT, amount NUMERIC);` <br> **Snowflake:** `CREATE TEMP TABLE temp_orders (id INT, amount NUMBER);` <br> **Oracle:** `CREATE GLOBAL TEMPORARY TABLE temp_orders (id NUMBER, amount NUMBER) ON COMMIT PRESERVE ROWS;` <br> **SQL Server:** `CREATE TABLE #temp_orders (id INT, amount DECIMAL(10,2));` | Enterprise: temporary tables reduce I/O on permanent tables and are session-scoped or transaction-scoped. |
| **Scope / Lifetime**                           | Defines how long temp data exists                   | PostgreSQL/SQLite/Snowflake: session <br> Oracle: session or commit-based (ON COMMIT DELETE ROWS / PRESERVE ROWS) <br> SQL Server: local temp `#temp` = session, global temp `##temp` = all sessions                                                                                                                                                                                                                                | Enterprise: choose scope based on workflow; avoid unnecessary session-wide temp tables.                   |
| **Insert / Query Temp Table**                  | Use temp table like regular table                   | \`\`\`sql                                                                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                           |
| INSERT INTO temp\_orders VALUES (1, 100.0);    |                                                     |                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                           |
| SELECT \* FROM temp\_orders WHERE amount > 50; |                                                     |                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                           |

````| Enterprise: temporary tables behave like regular tables but avoid permanent storage and reduce locking. |
| **Drop Temp Table** | Remove temporary table manually | `DROP TABLE temp_orders;` | Enterprise: usually auto-dropped at session end; manual drop frees resources early. |
| **Variables (Session / Local)** | Store single value or calculation | **PostgreSQL:** `DO $$ DECLARE v_total NUMERIC := 0; BEGIN v_total := 100; END $$;` <br> **SQL Server:** `DECLARE @v_total DECIMAL(10,2); SET @v_total = 100;` <br> **Oracle:** `DECLARE v_total NUMBER := 0; BEGIN v_total := 100; END;` <br> **Snowflake:** `SET v_total = 100;` | Enterprise: use variables for dynamic scripts, loops, and procedural logic. |
| **Variable Scope** | Session or block level | PostgreSQL/Oracle: block-level in `DO` or `PL/pgSQL`/`PLSQL` <br> SQL Server: batch or procedure-level <br> Snowflake: session-level using `SET` | Enterprise: minimize scope to reduce conflicts and memory usage. |
| **Use in Queries** | Parameterize or calculate | PostgreSQL/Oracle/SQL Server: use within procedural blocks or scripts <br> Snowflake: `SELECT $v_total;` | Enterprise: variables reduce hard-coded values and improve maintainability of scripts. |
| **Best Practices** | Efficient use of temp tables/variables | - Use temp tables for intermediate result sets in complex queries <br> - Keep temp tables small; index if reused <br> - Drop temp tables manually if done early <br> - Use variables for calculations, thresholds, or dynamic SQL <br> - Avoid session-wide temp tables unless necessary | Enterprise: improves performance, avoids permanent table clutter, and supports complex ETL/data processing workflows. |

---

## **Enterprise Design Notes**
- **SQLite:** Supports temp tables and in-memory storage; no procedural variables.  
- **PostgreSQL:** Fully supports temp tables, `DO` blocks, and procedural variables with `PL/pgSQL`.  
- **Snowflake:** Temp tables auto-drop at session end; variables via `SET` are session-level.  
- **Oracle:** Global temporary tables; variables in PL/SQL blocks; supports ON COMMIT behaviors.  
- **SQL Server:** Local (`#`) and global (`##`) temp tables; variables via `DECLARE`; fully supports procedural scripts and batch processing.  
- **Best Practices:**  
  - Prefer **temporary tables** over permanent staging tables for intermediate calculations.  
  - Scope **variables** as narrowly as possible.  
  - Use **indexes** on temp tables if reused in multiple queries for performance.  
  - Combine temp tables and variables in ETL scripts for efficiency and readability.  

---

## **Quick Examples**

```sql
-- PostgreSQL temp table
CREATE TEMP TABLE temp_orders (id INT, amount NUMERIC);
INSERT INTO temp_orders VALUES (1, 100.0);
SELECT * FROM temp_orders;
DROP TABLE temp_orders;

-- SQL Server temp table
CREATE TABLE #temp_orders (id INT, amount DECIMAL(10,2));
INSERT INTO #temp_orders VALUES (1, 100.0);
SELECT * FROM #temp_orders;

-- Oracle global temporary table
CREATE GLOBAL TEMPORARY TABLE temp_orders (
  id NUMBER,
  amount NUMBER
) ON COMMIT PRESERVE ROWS;

-- PostgreSQL variable in DO block
DO $$
DECLARE v_total NUMERIC := 0;
BEGIN
  v_total := 100;
  RAISE NOTICE 'Total = %', v_total;
END $$;

-- SQL Server variable
DECLARE @v_total DECIMAL(10,2);
SET @v_total = 100;
SELECT @v_total;

-- Snowflake temp table and variable
CREATE TEMP TABLE temp_orders (id INT, amount NUMBER);
SET v_total = 100;
SELECT $v_total;
````

---

This cheat sheet **covers all essential temporary tables and variable operations across major DBs**, highlighting **creation, scope, session behavior, usage in queries, and best practices**, making it **enterprise-ready for procedural scripts, ETL workflows, and intermediate data processing**.

