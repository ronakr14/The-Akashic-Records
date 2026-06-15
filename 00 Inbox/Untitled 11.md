# 1. Extraction Strategies
A lot of candidates say:
> "Extract data from source."
Interviewers may ask *how*.
### Types of extraction
#### Full Extraction
```text
Read entire table
```
Example:
```sql
SELECT * FROM customers
```
Pros:
* Simple
Cons:
* Expensive
---
#### Incremental Extraction
```text
Read only changes
```
Example:
```sql
SELECT *
FROM customers
WHERE updated_at > last_run_time
```
Pros:
* Fast
Cons:
* More complex
---
#### CDC Extraction
Database tells you exactly what changed.
```text
INSERT
UPDATE
DELETE
```
captured from transaction logs.