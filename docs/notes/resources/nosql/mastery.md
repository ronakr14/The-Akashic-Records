# Master

**NoSQL (Not Only SQL)** represents a set of **non-relational database systems** that prioritize:

- **Schema flexibility** (no rigid tables)
- **Horizontal scaling**
- **High-speed reads/writes at scale**

You’ll find NoSQL powering:

- Recommendation engines (MongoDB)
- Real-time analytics (Cassandra)
- Session stores and caches (Redis)
- Search indexing (Elasticsearch)
- Graph analysis (Neo4j)

NoSQL matters because relational models crack under:

- Unpredictable schema evolution
- Massive concurrent writes
- Geographically distributed systems
  SQL's strictness is a bottleneck there.

## 📊 SQL vs NoSQL Quick Contrast

| Feature        | SQL              | NoSQL                             |
| -------------- | ---------------- | --------------------------------- |
| Schema         | Fixed (strict)   | Dynamic (schema-less/flexible)    |
| Scaling        | Vertical         | Horizontal (sharding/replication) |
| Transactions   | ACID             | BASE                              |
| Data Types     | Tables/Relations | JSON, Key-Value, Graph, etc.      |
| Query Language | SQL              | Varies (MongoQL, Cypher, etc.)    |
| Use Cases      | OLTP, Reporting  | Big Data, Real-time, Caching      |