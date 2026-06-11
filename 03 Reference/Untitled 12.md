# 2. Watermarking
A surprisingly common topic.
Example:
```text
Last successful run:
2026-06-01 10:00
```
Next run:
```sql
SELECT *
FROM orders
WHERE modified_time >
'2026-06-01 10:00'
```
The stored timestamp is the watermark.
Questions:
* Where do you store it?
* What happens if job fails?