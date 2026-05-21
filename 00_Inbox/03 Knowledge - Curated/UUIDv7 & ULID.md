```table-of-contents
```
# Summary

UUIDv7 and ULID are **time-ordered unique ID formats** that give you **global uniqueness + chronological sorting**, which classic UUIDv4 absolutely does not.

# What problem does this solve?

Traditional UUIDs (v4):
1. Are random
2. Don’t sort by time
3. Fragment database indexes
4. Destroy write performance

Distributed systems need:
> “Unique IDs that scale AND sort.”

UUIDv7 and ULID solve this by embedding **time into the ID**.

# Mental Model

Think of UUIDv7 / ULID as:
> “Snowflake IDs, but standardized.”

Every new ID is slightly larger than the last.

# Where should I use this?

Use them when:
1. You build databases
2. You use distributed systems
3. You write event logs
4. You build APIs
5. You build data pipelines
6. You need pagination

Perfect for:
- Postgres PKs
- Kafka keys
- Event stores
- S3 object IDs
- Snowflake / Redshift keys

# When should I NOT use this?

Don’t use them when:
1. You don’t care about ordering
2. You want small integers
3. You rely on auto-increment IDs
4. You don’t have distributed writers

UUIDv7 is **overkill for monoliths**.

# What actually breaks it?

They break when:
1. System clocks drift
2. You generate too many IDs per millisecond
3. You depend on strict monotonicity
4. Time goes backwards

Time is now part of your data.

# Key tradeoffs

| **You choose** |      **You get**       |
|:-------------- |:----------------------:|
| UUIDv7         |      Standardized      |
| ULID           |     Human-friendly     |
| UUIDv4         |      Random chaos      |
| Auto-increment | Single-node bottleneck |

UUIDv7 = **future-proof**
ULID = **developer-friendly**