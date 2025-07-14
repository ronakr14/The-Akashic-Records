---
id: 2k075ofl6ekdhqtam0zf2eg
title: Roadmap
desc: ''
updated: 1752471189701
created: 1752471188763
---

Focus on **database models** + **real-world tradeoffs**.

| Stage | Focus Area                                  | Why?                                                           |
| ----- | ------------------------------------------- | -------------------------------------------------------------- |
| **1** | **Document Stores (MongoDB)**               | Most common entry-point to NoSQL. JSON-like flexibility.       |
| **2** | **Key-Value Stores (Redis, DynamoDB)**      | Session stores, counters, queues. Think microservices.         |
| **3** | **Wide-Column Stores (Cassandra, HBase)**   | Real-time analytics at petabyte scale.                         |
| **4** | **Graph Databases (Neo4j, Amazon Neptune)** | For relationships-heavy queries.                               |
| **5** | **Search Engines (Elasticsearch)**          | Text search, full-text indexing, log analytics.                |
| **6** | **CAP Theorem + BASE Consistency**          | Core of NoSQL tradeoff thinking.                               |
| **7** | **Data Modeling Patterns**                  | Single-table design (DynamoDB), aggregation pipelines (Mongo). |
| **8** | **Sharding, Replication**                   | Scaling & high availability.                                   |
