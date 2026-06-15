# 4. File Formats
Surprisingly common interview topic.
### Questions
Difference between:
* CSV
* JSON
* Avro
* Parquet
* ORC
Expected answer:
Parquet is columnar.
Why does that matter?
Because analytics often read:
```sql
SELECT revenue
FROM sales
```
rather than all columns.