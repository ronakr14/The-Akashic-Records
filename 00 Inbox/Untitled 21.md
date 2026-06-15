# 11. Idempotency
One of the most important ETL concepts.
Definition:
Running pipeline twice gives same result.
Bad:
```text
Run 1 -> 100 rows
Run 2 -> 200 rows
```
Good:
```text
Run 1 -> 100 rows
Run 2 -> 100 rows
```