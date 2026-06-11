# 5. Soft Delete vs Hard Delete
### Hard Delete
```text
Record removed
```
---
### Soft Delete
```text
is_deleted = true
```
Very common in ETL.
Questions:
* How do you propagate deletes?
* How does CDC handle deletes?