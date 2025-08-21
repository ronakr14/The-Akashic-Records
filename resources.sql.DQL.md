---
id: nkqm4yx3c0h0sjyf9pzbvn3
title: DQL
desc: ''
updated: 1755756636111
created: 1755756630029
---

# **Enterprise Multi-DB DQL (Data Query Language) Cheat Sheet**

| DQL Operation                      | Purpose                                  | Syntax                                                                                                                                                                                            | DB Notes / Enterprise Tips                                                                                                  |                                                                                                 |
| ---------------------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Simple SELECT**                  | Retrieve columns from a table            | `SELECT col1, col2 FROM table_name;`                                                                                                                                                              | Always specify columns instead of `SELECT *` for performance.                                                               |                                                                                                 |
| **Filtering / WHERE**              | Filter rows based on conditions          | `SELECT * FROM table_name WHERE condition;`                                                                                                                                                       | Supports `=, <>, >, <, >=, <=, IN, BETWEEN, LIKE, IS NULL` across all DBs.                                                  |                                                                                                 |
| **DISTINCT**                       | Remove duplicates                        | `SELECT DISTINCT col1, col2 FROM table_name;`                                                                                                                                                     | Useful for reporting queries.                                                                                               |                                                                                                 |
| **ORDER BY**                       | Sort results                             | \`SELECT \* FROM table\_name ORDER BY col1 ASC                                                                                                                                                    | DESC;\`                                                                                                                     | Multiple columns allowed; DB-specific NULL ordering (`NULLS FIRST/LAST` in PostgreSQL, Oracle). |
| **LIMIT / OFFSET / FETCH**         | Pagination                               | PostgreSQL / SQLite / MySQL: `LIMIT 10 OFFSET 20;` <br> SQL Server: `OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;` <br> Oracle: `FETCH FIRST 10 ROWS ONLY` or `OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY` | Enterprise: always use ORDER BY with pagination to guarantee deterministic results.                                         |                                                                                                 |
| **JOINs**                          | Combine tables                           | `INNER / LEFT / RIGHT / FULL OUTER JOIN table2 ON table1.col = table2.col;`                                                                                                                       | SQLite: no RIGHT/FULL JOIN; other DBs fully supported. Use aliases for clarity.                                             |                                                                                                 |
| **Aggregates**                     | Compute summary                          | `SELECT COUNT(*), SUM(col), AVG(col), MIN(col), MAX(col) FROM table_name;`                                                                                                                        | Combine with GROUP BY for grouped aggregation.                                                                              |                                                                                                 |
| **GROUP BY / HAVING**              | Aggregate grouped data                   | `SELECT col, SUM(amount) FROM table GROUP BY col HAVING SUM(amount) > 1000;`                                                                                                                      | HAVING filters post-aggregation; use for enterprise reporting.                                                              |                                                                                                 |
| **Subqueries / Nested SELECTs**    | Query within query                       | `SELECT * FROM table WHERE col IN (SELECT col FROM table2 WHERE ...);`                                                                                                                            | Can be correlated or uncorrelated; supported in all DBs.                                                                    |                                                                                                 |
| **CTEs (WITH)**                    | Define temporary named result sets       | `WITH cte AS (SELECT ...) SELECT * FROM cte WHERE ...;`                                                                                                                                           | PostgreSQL, SQL Server, Oracle, Snowflake support; SQLite supports WITH (>=3.8.3). Use for modular queries and readability. |                                                                                                 |
| **Window Functions**               | Ranking, running totals, moving averages | `SELECT col, ROW_NUMBER() OVER(PARTITION BY col2 ORDER BY col3) AS rn FROM table;`                                                                                                                | Supported in PostgreSQL, SQL Server, Oracle, Snowflake. SQLite (>=3.25) supports window functions.                          |                                                                                                 |
| **UNION / INTERSECT / EXCEPT**     | Combine result sets                      | `SELECT col FROM t1 UNION SELECT col FROM t2;`                                                                                                                                                    | UNION removes duplicates; UNION ALL keeps duplicates. INTERSECT/EXCEPT not in SQLite (use workarounds).                     |                                                                                                 |
| **CASE / Conditional Expressions** | Conditional logic in SELECT              | `SELECT CASE WHEN col > 0 THEN 'positive' ELSE 'non-positive' END AS col_status FROM table;`                                                                                                      | Supported in all DBs. Useful for reporting and derived columns.                                                             |                                                                                                 |

---

## **Enterprise Design Notes**

* **SQLite:** Supports basic SELECT, JOINs, aggregates, CTEs, window functions (>=3.25). Missing RIGHT/FULL JOIN and some set operations.
* **PostgreSQL:** Fully-featured DQL; advanced window functions, CTEs, JSON querying, filtering, and analytical functions.
* **Snowflake:** Cloud-native; supports semi-structured data queries (VARIANT), window functions, CTEs, and performance optimization via clustering keys.
* **Oracle:** Enterprise-grade; robust window functions, analytic queries, hierarchical queries (`CONNECT BY`), and CTEs.
* **SQL Server:** Supports ranking, window functions, TOP/N, OFFSET/FETCH, and CTEs.
* **Best Practices:**

  * Always specify explicit columns.
  * Use indexed columns in WHERE/JOIN clauses for performance.
  * Wrap complex queries in CTEs for readability and maintainability.
  * Use pagination for large result sets.
  * Document queries for enterprise ETL/reporting pipelines.

---

## **Quick Examples**

```sql
-- Simple select with filter
SELECT id, username, email
FROM users
WHERE status = 'active';

-- Join with aggregate
SELECT u.id, u.username, COUNT(o.id) AS total_orders
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username
HAVING COUNT(o.id) > 0;

-- CTE for modular query
WITH recent_orders AS (
    SELECT * FROM orders WHERE order_date > CURRENT_DATE - INTERVAL '30 days'
)
SELECT u.username, SUM(ro.amount) AS total
FROM users u
JOIN recent_orders ro ON u.id = ro.user_id
GROUP BY u.username;

-- Window function
SELECT username, order_date,
       ROW_NUMBER() OVER(PARTITION BY username ORDER BY order_date DESC) AS rn
FROM orders;

-- Conditional / CASE expression
SELECT username,
       CASE WHEN total_orders > 10 THEN 'VIP' ELSE 'Regular' END AS customer_type
FROM customer_summary;

-- Pagination (PostgreSQL / SQLite)
SELECT * FROM users ORDER BY created_at DESC LIMIT 10 OFFSET 20;

-- Pagination (SQL Server)
SELECT * FROM users ORDER BY created_at DESC OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;
```

---

This cheat sheet **covers all essential DQL operations across major DBs**, highlighting **differences in joins, window functions, CTEs, set operations, and pagination**, making it **enterprise-ready for reporting, analytics, and ETL pipelines**.
