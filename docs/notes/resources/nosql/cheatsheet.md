# Cheatsheet

- **MongoDB Aggregation**:

```js
db.orders.aggregate([
  { $match: { status: "completed" } },
  { $group: { _id: "$userId", totalSpent: { $sum: "$amount" } } }
])
```

- **Redis Core Ops**:

```bash
SET user:1001 "Ronak"
GET user:1001
INCR counter
EXPIRE session:xyz 3600
```

- **CAP Theorem**:

- **C**onsistency

- **A**vailability

- **P**artition Tolerance
  Pick **two**. No database can give all three simultaneously in a distributed setup.

- **DynamoDB Single-Table Design Rule**:
  Store **everything** in one table using composite keys (PK, SK). Think access patterns first, schema later.