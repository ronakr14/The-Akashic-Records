---
id: s4txl0tm3mhi8zktwy83eto
title: Dynamodb
desc: ''
updated: 1754050997528
created: 1754050993221
---
tags: [master, aws, dynamodb, nosql, cloud-database, serverless, key-value-store]

---

## 📌 Topic Overview

**Amazon DynamoDB** is a **fully managed NoSQL database** service by AWS, designed for **serverless, high-performance, low-latency** applications.

- It's a **key-value and document database**
- Offers **millisecond response times** at any scale
- Automatically handles **replication, backups, scaling**
- Widely used for gaming, IoT, mobile apps, ML features, event-driven systems

> Think: DynamoDB is AWS’s answer to the “I need ultra-fast, zero-maintenance, planet-scale data” question.

---

## 🚀 80/20 Roadmap

| Stage | Concept                         | Why It Matters                                   |
|-------|----------------------------------|--------------------------------------------------|
| 1️⃣    | Table Design (PK/SK, Schema)     | Core to performance, access, and scaling         |
| 2️⃣    | Basic CRUD via SDK/Boto3        | Power your apps and services                     |
| 3️⃣    | Query vs Scan                   | Avoid full scans for high throughput             |
| 4️⃣    | GSIs and LSIs                   | Flexible indexing = flexible querying            |
| 5️⃣    | Capacity Modes + Autoscaling    | Control cost and performance                     |
| 6️⃣    | Streams + Lambda Triggers       | Event-driven workflows and audit trails          |
| 7️⃣    | TTL, Backups, and Global Tables | Ops and reliability across regions               |
| 8️⃣    | PartiQL and Transactions        | SQL-style access and atomic operations           |
| 9️⃣    | IAM & Fine-Grained Access       | Securing Dynamo at the row level                 |
| 🔟    | Modeling 1:N and N:N relations   | Complex data shapes in a NoSQL world             |

---

## 🛠️ Practical Tasks

- ✅ Create a table with `user_id` (PK) and `created_at` (SK)
- ✅ Insert and read items using Boto3
- ✅ Query items using `KeyConditionExpression`
- ✅ Add a GSI to query by `email` or `status`
- ✅ Set DynamoDB to on-demand mode and autoscaling
- ✅ Create a stream to trigger a Lambda on inserts
- ✅ Set TTL to auto-expire session records
- ✅ Use PartiQL to run SQL-like queries
- ✅ Implement conditional writes for safe updates
- ✅ Deploy a global table spanning `us-east-1` and `eu-west-1`

---

## 🧾 Cheat Sheets

### 🔹 Table Creation (Boto3)

```python
import boto3

dynamodb = boto3.client('dynamodb')

dynamodb.create_table(
  TableName='Users',
  KeySchema=[
    {'AttributeName': 'user_id', 'KeyType': 'HASH'},
    {'AttributeName': 'created_at', 'KeyType': 'RANGE'}
  ],
  AttributeDefinitions=[
    {'AttributeName': 'user_id', 'AttributeType': 'S'},
    {'AttributeName': 'created_at', 'AttributeType': 'S'}
  ],
  BillingMode='PAY_PER_REQUEST'
)
````

### 🔹 Insert / Read Item

```python
table = boto3.resource('dynamodb').Table('Users')

# Insert
table.put_item(Item={'user_id': '123', 'created_at': '2025-01-01', 'name': 'Ronak'})

# Read
response = table.get_item(Key={'user_id': '123', 'created_at': '2025-01-01'})
print(response['Item'])
```

### 🔹 Query with KeyCondition

```python
from boto3.dynamodb.conditions import Key

response = table.query(
    KeyConditionExpression=Key('user_id').eq('123')
)
```

### 🔹 Conditional Update

```python
table.update_item(
  Key={'user_id': '123', 'created_at': '2025-01-01'},
  UpdateExpression='SET balance = :val',
  ExpressionAttributeValues={':val': 1000},
  ConditionExpression='attribute_exists(user_id)'
)
```

---

## 🎯 Progressive Challenges

| Level           | Task                                                                |
| --------------- | ------------------------------------------------------------------- |
| 🥉 Beginner     | Create a DynamoDB table and insert 10 users                         |
| 🥈 Intermediate | Create a GSI and query using alternate key                          |
| 🥇 Advanced     | Build a Lambda-triggered audit log using DynamoDB Streams           |
| 🏆 Expert       | Design a DynamoDB model for a real-time chat app with global tables |

---

## 🎙️ Interview Q\&A

* **Q:** What’s the difference between GSI and LSI in DynamoDB?
* **Q:** How does DynamoDB scale automatically?
* **Q:** Why is `Scan` considered inefficient?
* **Q:** How can you enforce uniqueness in a DynamoDB table?
* **Q:** Explain partition keys and hot partitions.
* **Q:** When would you use DynamoDB over RDS?

---

## 🛣️ Next Tech Stack Recommendations

* **Step Functions + Lambda** — Serverless workflows that react to DynamoDB events
* **AppSync + DynamoDB** — Build real-time GraphQL APIs
* **DynamoDB Global Tables + CloudFront** — Globally distributed, low-latency APIs
* **OpenSearch** — For full-text search on top of DynamoDB
* **Amazon EventBridge** — Orchestrate event flows beyond just Lambda

---

## 🧠 Pro Tips

* **Composite keys** are your NoSQL joins — design them smart
* Use **ConditionExpression** to avoid overwrites or lost updates
* **Avoid Scans** in production unless you love latency and bills
* **GSIs cost** — only index what you query
* **Streams + Lambda** give you CQRS or async projections out-of-the-box
* Embrace **single-table design** for high scale, low maintenance systems

---

## 🧬 Tactical Philosophy

> **DynamoDB isn’t “just NoSQL”—it’s a battle-hardened, planet-scale, serverless beast.**

📦 Model your access patterns, not your data
⚡ Design for reads, write sparingly
🛠️ Let indexes + streams do the heavy lifting
🔐 Lock down with IAM + fine-grained auth
🌍 Scale horizontally with global tables

---

