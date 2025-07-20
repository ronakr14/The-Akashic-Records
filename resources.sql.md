---
id: 9iw0cnb0kblvnvv9tut83ce
title: SQL
desc: ''
updated: 1753022043245
created: 1753022032002
---

## 📌 Topic Overview

**SQL (Structured Query Language)** is the backbone of relational databases—think PostgreSQL, MySQL, SQL Server. It’s used everywhere: reporting dashboards, ETL pipelines, backend APIs, data warehouses, and modern lakehouses. In your data engineer role, SQL isn’t optional—it’s your bread and butter.

SQL matters because:

* It’s declarative—**you tell the database what you want, not how.**
* It powers **data extraction, transformation, analysis,** and **reporting.**
* SQL is evolving: from simple SELECTs to **window functions, CTEs, analytical OLAP queries, and JSON processing.**

---

## ⚡ 80/20 Roadmap

Focus on **10x operators**—skills that cover 80% of your day-to-day and interview needs.

| Stage  | Focus Area                                                     | Why?                                                |
| ------ | -------------------------------------------------------------- | --------------------------------------------------- |
| **1**  | SELECT, WHERE, GROUP BY, ORDER BY, LIMIT                       | Absolute basics, but write them **blazingly fast**. |
| **2**  | INNER JOIN, LEFT JOIN, RIGHT JOIN                              | You can’t avoid joins in real-world schemas.        |
| **3**  | Subqueries, CTEs (`WITH` clause)                               | For readable, modular SQL. CTEs are your functions. |
| **4**  | Window Functions (`ROW_NUMBER()`, `RANK()`, `LEAD()`, `LAG()`) | Transformative for analytical querying.             |
| **5**  | Aggregations (SUM, COUNT, CASE WHEN)                           | KPI generation essentials.                          |
| **6**  | Indexing, EXPLAIN ANALYZE                                      | For query optimization and speed.                   |
| **7**  | JSON Processing (`JSON_EXTRACT()`, `->`, `->>`)                | Modern databases store semi-structured data.        |
| **8**  | Transactions, Isolation Levels                                 | Handle concurrency safely.                          |
| **9**  | Stored Procedures, Functions                                   | When SQL isn’t enough.                              |
| **10** | Partitioning, Sharding (Theoretical)                           | For scaling databases in enterprise setups.         |

---

## 🚀 Practical Tasks

| Task                                                                                                       | Description |
| ---------------------------------------------------------------------------------------------------------- | ----------- |
| 🔥 Write 20 complex queries using joins + window functions on a dummy e-commerce dataset.                  |             |
| 🔥 Use CTEs to refactor any spaghetti subquery into readable steps.                                        |             |
| 🔥 Take 5 slow queries and profile them using `EXPLAIN ANALYZE`. Optimize with indexing or query rewrites. |             |
| 🔥 Handle JSON columns using PostgreSQL or MySQL—extract nested keys, aggregate JSON data.                 |             |
| 🔥 Simulate dirty reads and phantom reads using isolation levels in PostgreSQL.                            |             |

---

## 🧾 Cheat Sheets

* **Window Functions**:
  `ROW_NUMBER() OVER(PARTITION BY … ORDER BY …)`
  `LAG(col) OVER(ORDER BY …)`
  `SUM(col) OVER(PARTITION BY …)`

* **Joins Summary**:
  `INNER JOIN` = Match both sides
  `LEFT JOIN` = Keep left, nulls from right
  `RIGHT JOIN` = Keep right, nulls from left
  `FULL JOIN` = Keep everything

* **CTE Structure**:

  ```sql
  WITH ranked_orders AS (
    SELECT *, ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY created_at DESC) as rn
    FROM orders
  )
  SELECT * FROM ranked_orders WHERE rn = 1;
  ```

* **JSON Extraction (PostgreSQL)**:
  `data -> 'key'` returns JSON object
  `data ->> 'key'` returns text

* **Query Optimization Steps**:

  1. Use proper indexes
  2. Reduce columns (`SELECT *` is evil)
  3. Avoid functions on indexed columns in WHERE
  4. Use `LIMIT` for paging

---

## 🎯 Progressive Challenges

| Level           | Challenge                                                                                       |
| --------------- | ----------------------------------------------------------------------------------------------- |
| 🥉 Easy         | Build a KPI report (Total sales, Top 5 products) using JOINs + GROUP BY.                        |
| 🥈 Intermediate | Write a SQL to calculate 7-day rolling average sales per product.                               |
| 🥇 Expert       | Simulate sessionization (user events) using `LAG()` + window functions. Generate event funnels. |
| 🏆 Black Belt   | Take a 5-way JOIN query and optimize it for sub-second response time. Use EXPLAIN plans.        |

---

## 🎙️ Interview Q\&A

* **Q:** Difference between `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()`?
* **Q:** Why does `LEFT JOIN` sometimes return more rows than the left table?
* **Q:** What’s the impact of indexing on SELECT vs. INSERT performance?
* **Q:** How do transactions prevent dirty reads?
* **Q:** Explain the query plan steps in PostgreSQL EXPLAIN ANALYZE.

---

## 🛣️ Next Tech Stack Recommendation

Once you’re SQL-fluent, expand into:

* **dbt (Data Build Tool)** — SQL-based transformation pipelines.
* **DuckDB** — Modern OLAP database, runs SQL locally.
* **ClickHouse** — Blazing fast analytical DB for large-scale OLAP workloads.
* **SparkSQL** — If you're working in big data environments.
* **SQLMesh** — dbt alternative for SQL-centric transformations.

