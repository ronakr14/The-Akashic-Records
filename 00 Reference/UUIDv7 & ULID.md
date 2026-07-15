# UUIDv7 & ULID

```table-of-contents
```

## What Problem Does This Solve?

Traditional UUIDs (v4):

1. Are random
2. Don't sort by time
3. Fragment database indexes
4. Destroy write performance

Distributed systems need: *"Unique IDs that scale AND sort."*

UUIDv7 and ULID solve this by embedding **time into the ID**.

---

## Mental Model

Think of UUIDv7 / ULID as: *"Snowflake IDs, but standardized."*

Every new ID is slightly larger than the last. Newer IDs sort after older IDs in lexicographic or numeric ordering.

---

## Format Specifications

### UUIDv7 (RFC 9562)

128 bits total:

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├─────────────┼───────┼─────────────────────────────────────────────�
  unix_ts_ms  ver   rand_a              rand_b
  (48 bits)  (4)   (12 bits)           (62 bits)
```

- **unix_ts_ms** (48 bits): Unix timestamp in milliseconds. Good until year 10,889.
- **ver** (4 bits): Always `0111` (7) for UUIDv7.
- **rand_a** (12 bits): Random bits.
- **rand_b** (62 bits): Random bits + variant bits.

Total: 122 random bits. ~5 × 10⁻¹⁸ collision probability per pair.

### ULID (Universally Unique Lexicographically Sortable Identifier)

26-character Crockford's Base32 encoded string:

```text
 01ARZ3NDEKTSV4RRFFQ69G5FAV
 ├──────────┼─────────────────────┤
  timestamp    randomness
  (48 bits)   (80 bits)
```

- **Timestamp** (48 bits): Unix epoch in milliseconds. Same range as UUIDv7.
- **Randomness** (80 bits): Cryptographically secure random.
- **Total length**: 26 characters (Base32, no padding, no hyphens).
- **Case-insensitive** — safe for URLs, filenames, logs.

### Key Difference

| Property | UUIDv7 | ULID |
|---|---|---|
| Binary size | 128 bits (16 bytes) | 128 bits (16 bytes) |
| String representation | 36 chars (with hyphens) | 26 chars (no hyphens) |
| Encoding | Hex | Crockford's Base32 |
| Human readability | Low | Higher |
| Standard | RFC 9562 (IETF) | Spec github (de facto) |

---

## Comparison

| Format | Size (string) | Sortable | Standard | Human-readable | Best for |
|---|---|---|---|---|---|
| UUIDv4 | 36 chars | No | RFC 4122 | Low | Legacy, non-indexed |
| UUIDv7 | 36 chars | Yes | RFC 9562 | Low | DB PKs, event IDs |
| ULID | 26 chars | Yes | De facto spec | Medium | URLs, logs, APIs |
| Snowflake | 18 digits | Yes | Twitter (de facto) | High | Internal systems |
| Auto-increment | 8–20 digits | Yes | None | High | Single-node DBs |

→ **Risk:** Using UUIDv4 as a primary key in a B-tree index causes severe page splits and fragmentation. UUIDv7/ULID eliminate this.

---

## When to Use

### Use UUIDv7 / ULID when:

- Distributed writers (multiple app servers generating IDs)
- Database primary keys (especially in distributed DBs)
- Event logs and event stores
- Kafka message keys
- S3 object IDs
- API-facing identifiers (ULID preferred for URLs)
- Pagination keys (cursor-based)

### Don't use when:

- Single-node database with auto-increment available
- Small dataset where integer PKs are sufficient
- You need minimal storage overhead (integers are smaller)
- Ordering doesn't matter

UUIDv7 is **overkill for monoliths**.

---

## When They Break

Time-dependent IDs have failure modes that random IDs don't:

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Clock drift | NTP issues, VM pauses | Use NTP with `-x` slew mode; monotonic clock |
| High throughput (>1M IDs/sec) | More IDs than random bits can distinguish per ms | Add sequence counter; use cryptographic RNG |
| Non-monotonic IDs | System clock goes backwards (DST, manual change) | Detect clock regression; wait or abort |
| Duplicate IDs | Broken RNG, VM clone with same seed | Seed from `/dev/urandom`; verify entropy source |

→ **Risk:** Time is now part of your data. Clock issues become data integrity issues.

---

## Implementation Examples

### Python

```python
# UUIDv7 (Python 3.14+)
import uuid
id = uuid.uuid7()

# UUIDv7 (older Python)
# pip install uuid7
import uuid7
id = uuid7.uuid7()

# ULID
# pip install python-ulid
from ulid import ULID
id = ULID()
str(id)  # 01ARZ3NDEKTSV4RRFFQ69G5FAV
```

### SQL (Postgres)

```sql
-- UUIDv7 (Postgres 16+)
SELECT gen_random_uuid();  -- v7 by default in PG16+

-- Or with extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;
SELECT gen_random_uuid();
```

### Java

```java
// UUIDv7 (Java 21+)
UUID id = UUID.randomUUID();  // returns v7 in Java 21+

// ULID
// Maven: de.huxhorn.sulky:ulid
ULID id = ULID.nextValue();
```

### Go

```go
// UUIDv7
import "github.com/google/uuid"
id := uuid.NewRandom()  // v7 since uuid v7.0

// ULID
import "github.com/oklog/ulid/v2"
id := ulid.Make()
```

---

## Database-Specific Guidance

### Postgres

| Approach | Pros | Cons |
|---|---|---|
| `uuid` type + UUIDv7 | Native support, 16 bytes, index-friendly | 36-char display |
| `bigint` + Snowflake | 8 bytes, fastest index | Not standard, needs generator |
| `text` + ULID | 26 chars, URL-safe | Slightly slower than uuid type |

```sql
-- Recommended: uuid type with v7 generation
CREATE TABLE events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    payload jsonb NOT NULL
);
```

### MySQL

MySQL lacks native UUID type. Use `BINARY(16)` for storage efficiency:

```sql
CREATE TABLE events (
    id BINARY(16) PRIMARY KEY,
    payload JSON NOT NULL
);

-- Insert UUIDv7 (convert to binary)
INSERT INTO events (id, payload)
VALUES (UNHEX(REPLACE(UUID(), '-', '')), '{"key": "value"}');
```

### Snowflake

```sql
-- Snowflake supports UUID natively
CREATE TABLE events (
    id VARCHAR(36) DEFAULT UUID_STRING(),
    payload VARIANT
);

-- Or use Snowflake's native sequential ID
CREATE TABLE events (
    id NUMBER(38, 0) AUTOINCREMENT,
    payload VARIANT
);
```

### Redshift

Redshift does not have a native UUID type. Use `CHAR(36)` or `BINARY(16)`:

```sql
CREATE TABLE events (
    id CHAR(36) DEFAULT uuid_generate_v4(),
    payload VARCHAR(MAX)
);
```

---

## Migration Path

### From UUIDv4 to UUIDv7

```sql
-- Add new column
ALTER TABLE events ADD COLUMN id_v7 uuid;

-- Backfill (one-time, in batches to avoid lock)
UPDATE events SET id_v7 = uuid_generate_v4() WHERE id_v7 IS NULL;

-- Or generate v7 in application code and update

-- Eventually: drop old column, rename new
ALTER TABLE events RENAME COLUMN id TO id_v4;
ALTER TABLE events RENAME COLUMN id_v7 TO id;
```

### From Auto-Increment to UUIDv7

```sql
-- Add UUID column (nullable first to avoid full table rewrite)
ALTER TABLE events ADD COLUMN id_uuid uuid;

-- Backfill in batches
UPDATE events
SET id_uuid = gen_random_uuid()
WHERE id_uuid IS NULL;

-- Set NOT NULL and add unique constraint
ALTER TABLE events ALTER COLUMN id_uuid SET NOT NULL;
ALTER TABLE events ADD CONSTRAINT uk_events_uuid UNIQUE (id_uuid);

-- Keep old column for backward compatibility during migration
-- Drop after all consumers updated
```

→ **Risk:** Migrating a large table with billions of rows takes hours and impacts production. Always add the new column first, backfill in batches, then switch over.

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| UUIDv4 as clustered PK | Index fragmentation, page splits | Use UUIDv7 or ULID |
| Storing UUIDs as VARCHAR | 2× storage, slower indexes | Use native UUID or BINARY(16) |
| Generating IDs in DB only | Limits scalability | Generate in application layer |
| Ignoring clock issues | Non-monotonic IDs, duplicates | Monitor NTP, use monotonic clock |
| Using ULID for DB PK in Postgres | No native type, slower than uuid type | Use uuid type with UUIDv7 |
| Exposing sequential IDs in URLs | Enumeration attacks, reveals volume | Use ULID or hash before exposing |
