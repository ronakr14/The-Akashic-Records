# 12. Exactly Once vs At Least Once
Frequently asked.
### At Least Once
May process duplicates.
```text
1..n times
```
---
### Exactly Once
Process record once only.
Harder.
Usually needs:
* Transactions
* Checkpointing
* Deduplication