# Cheatsheet

- **Window Functions**:
  `ROW_NUMBER() OVER(PARTITION BY … ORDER BY …)`
  `LAG(col) OVER(ORDER BY …)`
  `SUM(col) OVER(PARTITION BY …)`

- **Joins Summary**:
  `INNER JOIN` = Match both sides
  `LEFT JOIN` = Keep left, nulls from right
  `RIGHT JOIN` = Keep right, nulls from left
  `FULL JOIN` = Keep everything

- **CTE Structure**:

  ```sql
  WITH ranked_orders AS (
    SELECT *, ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY created_at DESC) as rn
    FROM orders
  )
  SELECT * FROM ranked_orders WHERE rn = 1;
  ```

- **JSON Extraction (PostgreSQL)**:
  `data -> 'key'` returns JSON object
  `data ->> 'key'` returns text

- **Query Optimization Steps**:

  1. Use proper indexes
  2. Reduce columns (`SELECT *` is evil)
  3. Avoid functions on indexed columns in WHERE
  4. Use `LIMIT` for paging