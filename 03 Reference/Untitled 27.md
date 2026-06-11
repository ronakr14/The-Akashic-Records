# 17. Push vs Pull ETL
### Pull
ETL reads source.
```text
ETL → Database
```
---
### Push
Source sends data.
```text
Application → ETL
```
Usually via:
* Events
* Kafka
* Webhooks