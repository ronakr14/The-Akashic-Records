---
id: vqeu8gso6rlwxooigopfgnk
title: Subquery
desc: ''
updated: 1755756917934
created: 1755756912654
---

# **Enterprise Multi-DB Subqueries Cheat Sheet**

| Subquery Type                           | Purpose                                                 | Syntax / Example                                                                                                                                                                                                 | DB Notes / Enterprise Tips                                                                                      |
| --------------------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Scalar Subquery**                     | Returns a single value for use in SELECT, WHERE, or SET | `SELECT username, (SELECT MAX(order_date) FROM orders o WHERE o.user_id = u.id) AS last_order FROM users u;`                                                                                                     | All major DBs support. Ensure subquery returns only one row to avoid errors.                                    |
| **Column Subquery**                     | Returns a single column (multiple rows)                 | `SELECT username FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > 100);`                                                                                                                        | Use in `IN`, `NOT IN`, `EXISTS`, `ANY`, `ALL`. SQLite, PostgreSQL, Oracle, SQL Server, Snowflake fully support. |
| **Row Subquery**                        | Returns a single row of multiple columns                | `SELECT * FROM users WHERE (id, username) = (SELECT id, username FROM temp_users WHERE id = 10);`                                                                                                                | Supported in PostgreSQL, Oracle; SQL Server uses `EXISTS` or joins. SQLite: limited tuple comparison.           |
| **Table/Subquery in FROM**              | Treat subquery as a derived table / CTE                 | `SELECT t.username, t.total_orders FROM (SELECT user_id, COUNT(*) AS total_orders FROM orders GROUP BY user_id) t JOIN users u ON u.id = t.user_id;`                                                             | Enterprise: improves modularity, reusable reporting queries.                                                    |
| **Correlated Subquery**                 | Subquery references outer query                         | `SELECT username FROM users u WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.amount > 100);`                                                                                                  | Often less performant than joins; indexes recommended.                                                          |
| **Uncorrelated / Independent Subquery** | Subquery runs independently                             | `SELECT username FROM users WHERE id IN (SELECT user_id FROM orders);`                                                                                                                                           | Can be optimized better; used for filtering or derived calculations.                                            |
| **EXISTS / NOT EXISTS**                 | Check existence efficiently                             | `SELECT username FROM users u WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);`                                                                                                                     | Preferred over `IN` for large datasets to avoid NULL pitfalls.                                                  |
| **ANY / ALL**                           | Compare against multiple rows                           | `SELECT username FROM users WHERE id = ANY (SELECT user_id FROM orders WHERE amount > 100);`                                                                                                                     | SQL Server uses `= ANY` / `> ALL`; PostgreSQL, Oracle, Snowflake fully support.                                 |
| **WITH / CTE Subquery**                 | Modular subquery with reusable alias                    | `WITH recent_orders AS (SELECT * FROM orders WHERE order_date > CURRENT_DATE - INTERVAL '30 days') SELECT u.username, COUNT(ro.id) FROM users u JOIN recent_orders ro ON u.id = ro.user_id GROUP BY u.username;` | Enterprise: improves readability, maintainability, and performance in complex analytics.                        |
| **Nested Subqueries**                   | Multiple levels                                         | `SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > (SELECT AVG(amount) FROM orders));`                                                                                                  | Enterprise: keep nesting shallow for performance; prefer joins/CTEs for clarity.                                |

---

## **Enterprise Design Notes**

* **SQLite:** Supports scalar, column, correlated subqueries, derived tables; limited row tuple comparison.
* **PostgreSQL:** Fully-featured; supports scalar, row, table, correlated, uncorrelated, CTEs, nested subqueries.
* **Snowflake:** Supports all subquery types; optimized for analytic workloads.
* **Oracle:** Full support; supports scalar, row, table, correlated, uncorrelated, CTEs, hierarchical subqueries.
* **SQL Server:** Full support; supports scalar, table, correlated, uncorrelated, nested subqueries, CTEs; some row subquery syntax differs.
* **Best Practices:**

  * Use **EXISTS** over `IN` for large datasets.
  * Prefer **CTEs / derived tables** over deep nested subqueries for readability.
  * Index foreign keys used in correlated subqueries to improve performance.
  * Avoid excessive nesting; flatten with joins or CTEs when possible.
  * Test subquery performance across DBs; optimizer behavior differs.

---

## **Quick Examples**

```sql
-- Scalar subquery
SELECT username, (SELECT MAX(order_date) FROM orders o WHERE o.user_id = u.id) AS last_order
FROM users u;

-- Column subquery
SELECT username
FROM users
WHERE id IN (SELECT user_id FROM orders WHERE amount > 100);

-- Correlated subquery with EXISTS
SELECT username
FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.amount > 100);

-- Table subquery / derived table
SELECT t.user_id, t.total_orders
FROM (SELECT user_id, COUNT(*) AS total_orders FROM orders GROUP BY user_id) t
JOIN users u ON u.id = t.user_id;

-- CTE subquery
WITH recent_orders AS (
    SELECT * FROM orders WHERE order_date > CURRENT_DATE - INTERVAL '30 days'
)
SELECT u.username, COUNT(ro.id)
FROM users u
JOIN recent_orders ro ON u.id = ro.user_id
GROUP BY u.username;

-- Nested subquery
SELECT * FROM users
WHERE id IN (
    SELECT user_id FROM orders
    WHERE amount > (SELECT AVG(amount) FROM orders)
);
```

---

This cheat sheet **covers all essential subquery operations across major DBs**, highlighting **scalar, column, row, table, correlated, uncorrelated, nested, and CTE subqueries**, making it **enterprise-ready for analytics, reporting, and ETL logic**.

