---
id: 6kngzpry9sahz5pb1jg4d6o
title: Joins
desc: ''
updated: 1755756139107
created: 1755756128345
---

# **Enterprise Multi-DB JOIN Cheat Sheet**

| Join Type                    | Purpose                                                  | Basic Syntax                                                                           | Notes / Enterprise Tips                                                                                        |
| ---------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **INNER JOIN**               | Return rows with matching keys in both tables            | `sql SELECT a.col1, b.col2 FROM table_a a INNER JOIN table_b b ON a.id = b.a_id;`      | Most common join. Filters unmatched rows.                                                                      |
| **LEFT / LEFT OUTER JOIN**   | Return all rows from left table, matched rows from right | `sql SELECT a.col1, b.col2 FROM table_a a LEFT JOIN table_b b ON a.id = b.a_id;`       | Nulls appear where right table has no match.                                                                   |
| **RIGHT / RIGHT OUTER JOIN** | Return all rows from right table, matched rows from left | `sql SELECT a.col1, b.col2 FROM table_a a RIGHT JOIN table_b b ON a.id = b.a_id;`      | SQLite does **not support RIGHT JOIN**; emulate with LEFT JOIN swap.                                           |
| **FULL / FULL OUTER JOIN**   | Return all rows from both tables                         | `sql SELECT a.col1, b.col2 FROM table_a a FULL OUTER JOIN table_b b ON a.id = b.a_id;` | SQLite does **not support FULL OUTER JOIN**; emulate with UNION of LEFT and RIGHT joins.                       |
| **CROSS JOIN**               | Cartesian product                                        | `sql SELECT a.col1, b.col2 FROM table_a a CROSS JOIN table_b b;`                       | All combinations; no ON clause. Use carefully with large tables.                                               |
| **SELF JOIN**                | Join a table to itself                                   | `sql SELECT a.id, b.id FROM employees a JOIN employees b ON a.manager_id = b.id;`      | Use aliases (`a`, `b`) to differentiate.                                                                       |
| **NATURAL JOIN**             | Join on columns with the same name                       | `sql SELECT * FROM table_a NATURAL JOIN table_b;`                                      | PostgreSQL, Oracle, Snowflake support; SQLite does too, but not recommended for enterprise—prefer explicit ON. |
| **USING clause**             | Join on column(s) with same name                         | `sql SELECT * FROM table_a JOIN table_b USING(id);`                                    | Cleaner than ON for same-name columns; supported in PostgreSQL, Oracle, Snowflake.                             |

---

## **Enterprise Design Notes**

* **SQLite Limitations:**

  * Does **not support RIGHT JOIN** or FULL OUTER JOIN natively. Use `LEFT JOIN` + `UNION ALL` or subqueries.
* **Outer joins:** Always handle `NULL` results carefully in SELECTs, WHERE clauses, and aggregates.
* **Aliasing:** Always alias tables in multi-join queries for clarity and maintainability.
* **JOIN Order / Performance:**

  * PostgreSQL, Snowflake, SQL Server, Oracle have query optimizers; join order may affect performance.
  * Consider indexes/clustered keys on join columns for performance.
* **Cross-database differences:**

  * Snowflake fully supports ANSI JOINs.
  * Oracle: Use `(+)=` old syntax only if legacy; prefer ANSI `JOIN`.
  * SQL Server: ANSI joins recommended over legacy comma joins.
* **Semi-structured joins:**

  * Snowflake supports `LATERAL FLATTEN()` for joining VARIANT arrays.
  * PostgreSQL supports `jsonb_array_elements()` for JSONB.

---

## **Quick Example Across Databases**

```sql
-- INNER JOIN
SELECT u.username, o.amount
FROM users u
INNER JOIN orders o
ON u.id = o.user_id;

-- LEFT JOIN
SELECT u.username, o.amount
FROM users u
LEFT JOIN orders o
ON u.id = o.user_id;

-- FULL OUTER JOIN (not SQLite)
SELECT u.username, o.amount
FROM users u
FULL OUTER JOIN orders o
ON u.id = o.user_id;

-- SELF JOIN example
SELECT e1.name AS employee, e2.name AS manager
FROM employees e1
LEFT JOIN employees e2
ON e1.manager_id = e2.id;
```

---

This is **compact and enterprise-ready**, showing **join types, syntax, DB support, and best practices** in one glance.
