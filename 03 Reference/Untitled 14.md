# 4. Load Patterns
This is often skipped.
---
### Append
```text
Add new rows
```
Example:
Logs.
---
### Overwrite
```text
Delete old data
Load new data
```
Common in reporting tables.
---
### Upsert
```text
Insert if missing
Update if exists
```
Example:
```sql
MERGE INTO target
```