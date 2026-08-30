# AI Summary
Comprehensive guide to stream processing, progressing from foundational concepts to production-scale architectures. Explains events, streams, Kafka, Flink, Spark Structured Streaming, event time, watermarks, windowing, stateful processing, fault tolerance, processing guarantees, joins, CDC, event-driven architecture, schema evolution, observability, replay, distributed systems, lakehouse streaming, and streaming design patterns. Includes mental models, real-world architectures, interview roadmap, advanced system design questions, and production best practices for building scalable real-time data platforms.

---
The easiest way to understand it is:
> **Batch Processing = Process data later**
> **Stream Processing = Process data as it arrives**

---

# Foundations

- Streams = continuous flow of events.
- Event = something that happened (purchase, login, sensor reading).
- Streaming processes data as it arrives; batch processes data later.

---

# 1. Start With a Real-Life Example

Imagine an e-commerce website.
Users are:
- Visiting products    
- Adding items to cart    
- Making purchases    
- Leaving reviews    
Every action generates data.

## Batch World
You collect all events during the day.
At midnight:
```text
Day's Events
      ↓
Store in Database
      ↓
Run ETL Job
      ↓
Generate Reports
```
Result:
```text
Today's sales report available tomorrow morning
```

---

## Streaming World
As soon as an order happens:
```text
Order Created
     ↓
Event Generated
     ↓
Processed Immediately
     ↓
Dashboard Updated
```
Result:
```text
Sales dashboard updates in seconds
```

---

# 2. What Is a Stream?

Think of a stream like flowing water.
Instead of receiving a file:
```text
sales.csv
```
you continuously receive:
```text
Order #1
Order #2
Order #3
Order #4
...
```
Never-ending data.
```text
Event → Event → Event → Event → Event
```
This continuous flow is called a **stream**.

---

# 3. What Is an Event?

Everything in streaming revolves around events.
An event is simply:
> Something that happened.

Example:
```json
{
  "event_id": 123,
  "user_id": 45,
  "action": "purchase",
  "amount": 200,
  "timestamp": "2026-06-03T10:15:00"
}
```
Examples:
- User login
- Payment completed
- Sensor reading
- GPS location update
- Stock price change

---

# 4. Core Architecture

```text
Producer → Message Broker → Stream Processor → Storage/Analytics
```

## Producer
Produces events.
Examples:
- Mobile app
- Website
- IoT sensor
- Payment service
```text
User clicks Buy
      ↓
Event Produced
```

## Message Broker
Stores and transports events.
Popular tools:
- Apache Kafka
- Apache Pulsar
- RabbitMQ
Think of Kafka as:
```text
Digital Post Office
```
Producers drop messages.
Consumers pick them up.

## Stream Processor
Reads events and performs computations.
Popular tools:
- Apache Flink
- Apache Spark Structured Streaming
- Apache Beam
Example:
```text
Purchase Event
       ↓
Calculate Revenue
       ↓
Update Dashboard
```

---

# 5. Why Streaming Exists

Traditional batch jobs are too slow for some use cases.

## Fraud Detection
Batch:
```text
Detect fraud tomorrow
```
Bad.

Streaming:
```text
Transaction happens
      ↓
Detect fraud immediately
      ↓
Block card
```
Good.

## Ride Sharing
```text
Driver location updates
Every few seconds
```
Need real-time processing.
Batch is useless.

## Stock Trading
Prices change every second.
Need instant reaction.

---

# 6. Essential Concepts

## Time

- **Event Time**: when event actually happened (timestamp inside event).
- **Processing Time**: when system processed it.
- **Ingestion Time**: when event entered the platform.

Real-world systems prefer **Event Time** because networks delay data.

## Late Arriving Data

Suppose:
```text
Event A -> arrives instantly
Event B -> arrives 10 minutes late
```
Can happen because:
- network issues
- mobile offline mode
- retries

Example:
```text
10:00 purchase
10:12 arrives
```
Processor must handle this.
This is a major streaming challenge.

## Windowing

Streams never end.
How do you calculate:
```text
Revenue per hour
```
if data never stops?
Use windows.

### Tumbling Window
Fixed non-overlapping windows.
```text
10:00 - 11:00
11:00 - 12:00
12:00 - 01:00
```
Example:
```sql
SUM(amount)
GROUP BY 1 hour
```

```text
|---1 hr---|
|---1 hr---|
|---1 hr---|
```

### Sliding Window
Overlapping windows.
Example:
```text
Window = 10 mins
Slide = 1 min
```
Produces more granular metrics.

```text
0-10
1-11
2-12
3-13
```

### Session Window
Groups activity separated by inactivity.
Example:
User browsing.
```text
10:00 click
10:01 click
10:03 click
```
No activity:
```text
30 mins
```
New session starts.

### Advanced Windows
- **Custom windows**: e.g. Market Open → Market Close instead of fixed hours.
- **Dynamic windows**: VIP Users → 1 min window, Normal Users → 30 min window.
- **Window triggers**: fire early (every 10 seconds) while window remains open.
- **Window eviction**: remove old records before final aggregation for memory optimization.

## Watermarks

One of the hardest concepts.
Problem:
```text
Events arrive late
```
How long should we wait?
Forever?
Impossible.

Watermark says:
> "I believe I have received most events up to this time."

Example:
```text
Current event time: 10:30
Watermark:
10:25
```
Meaning:
```text
Anything before 10:25
is probably complete
```
Window can close.
This prevents waiting forever.

### Advanced Watermark Topics
- Idle partitions
- Watermark propagation
- Watermark alignment across partitions
- Global watermark calculation
- Watermark skew

Example:
```text
Partition A watermark = 10:00
Partition B watermark = 09:50
```
Question:
```text
What should the operator watermark be?
```

## Stateful Processing

### Stateless
```text
Event
 ↓
Transform
 ↓
Output
```
No memory.
Example:
```python
convert_currency(event)
```

### Stateful
Remembers previous events.
Example:
```text
Running total sales
```
Need memory:
```text
100
200
300
400
```
Current total:
```text
1000
```

Examples:
- running counts
- sessions
- fraud detection
- aggregates

### State Types
- **Keyed State**: each key owns its own state (User A → state, User B → state).
- **Operator State**: shared state across operator instances.
- **Broadcast State**: rules, configurations, reference data — updates all processors dynamically.

### State Lifecycle Management
- **State TTL**: automatically remove old state (user inactive for 30 days → delete state).
- **State Cleanup**: during checkpoint, during access, or both.
- **State Migration**: what happens when job is upgraded but state already exists?

---

# 7. Processing Guarantees

## At Most Once
```text
May lose data
No duplicates
```

## At Least Once
```text
No data loss
Duplicates possible
```
Most common.

## Exactly Once
```text
No loss
No duplicates
```
Hardest.
Modern tools like Kafka + Flink support this.

### Deeper Guarantee Topics
- **Deterministic Processing**: can results be reproduced?
- **Idempotency**: can duplicate events be safely processed?
- **Transactional Sinks**: can state and output commit atomically?

---

# 8. Fault Tolerance

## Checkpoints
Save state periodically.
```text
State = 1,000,000 events processed
```
Crash.
Restart.
Continue from checkpoint.

### Advanced Fault Tolerance
- **Incremental checkpoints**: only save changes since last checkpoint (cheaper than full).
- **Savepoints**: different from checkpoints; used for job upgrades, migration.
- **Barrier Alignment**: core Flink concept for consistent checkpoints.
- **Unaligned Checkpoints**: solve severe backpressure issues during checkpointing.
- **Recovery and replay**: how to rebuild state from Kafka after failure.

---

# 9. Stream Joins

## Stream-Stream Join
```text
Orders
JOIN
Payments
```

## Stream-Table Join
```text
Orders Stream
JOIN
Customer Table
```

## Temporal Join
Join using historical version.
Example:
```text
Customer Tier
```
at the time order was placed.
Not current value.

## Interval Join
Join only within time bounds.
Example:
```text
Order
Payment
within 10 minutes
```

---

# 10. Scaling Challenges

- **State redistribution during rescaling**: 8 → 64 workers requires moving state.
- **Hot keys and partition skew**: one user generates 70% of traffic.
- **Backpressure propagation**: slow sink affects entire pipeline upstream.
- **Large-state management**: 500 million users, each with state.

## Backpressure Mechanics
```text
Source
 ↓
Map
 ↓
Aggregate
 ↓
Sink
```
Sink slows.
What happens upstream?
How do queues fill?
How is throughput affected?

---

# 11. Stream vs Batch

|Feature|Batch|Streaming|
|---|---|---|
|Latency|Hours|Seconds/Milliseconds|
|Data|Historical|Continuous|
|Complexity|Lower|Higher|
|Cost|Lower|Higher|
|Real-time|No|Yes|

---

# 12. Typical Modern Data Engineering Streaming Stack

```text
Applications
      ↓
Kafka
      ↓
Flink
      ↓
Iceberg
      ↓
DuckDB / Spark / Trino
      ↓
BI Dashboard
```
Flow:
```text
Events
 ↓
Kafka
 ↓
Real-Time Processing
 ↓
Lakehouse
 ↓
Analytics
```

---

# 13. What a Data Engineer Actually Does

### Ingestion
```text
App → Kafka
```
Design topics and schemas.

### Processing
```text
Kafka → Flink
```
Implement:
- aggregations
- joins
- deduplication
- enrichment

### Storage
```text
Flink → Iceberg
```
Store processed data.

### Monitoring
Track:
- lag
- throughput
- failures
- latency

---

# 14. Mental Model

Think of streaming as a factory conveyor belt:
```text
Batch:
Process all boxes tonight
Streaming:
Process every box
while it is moving
on the conveyor belt
```
Once that picture clicks, concepts like Kafka topics, windows, watermarks, state, checkpoints, and exactly-once processing become much easier to understand.

## The Core Idea

Batch: Recompute everything.
Streaming: Update only what changed.

Example:
Revenue:
```text
Yesterday = 1000
New Order = 50
Result = 1050
```
instead of recalculating all sales.
This is arguably the most important mental model in stream processing.

---

# 15. Advanced Topics

## Event-Driven Architecture (EDA)
Most streaming systems are actually event-driven systems.
```text
Order Service
      ↓
OrderCreated Event
      ↓
Inventory Service
      ↓
Payment Service
      ↓
Notification Service
```
Key concepts:
- Event sourcing
- CQRS
- Event choreography
- Event orchestration

## Change Data Capture (CDC)
One of the most common real-world streaming patterns.
```text
Postgres
    ↓
Debezium
    ↓
Kafka
    ↓
Flink
    ↓
Iceberg
```

## Data Contracts & Schema Evolution
One of the biggest production problems.
Version 1:
```json
{
 "user_id":123
}
```
Version 2:
```json
{
 "customer_id":123
}
```
Pipeline breaks.
Topics:
- Forward compatibility
- Backward compatibility
- Schema registry
- Contract testing
Tools:
- Apache Avro
- Protocol Buffers
- Apache Kafka Schema Registry

## Lakehouse Streaming
This is where data engineering is moving.
```text
Kafka
 ↓
Flink
 ↓
Iceberg
 ↓
Trino
 ↓
BI
```

## Data Quality in Streaming
Questions:
- How do you detect duplicates?
- Missing events?
- Out-of-order events?
- Corrupt events?

## Streaming Observability
Metrics:
### Consumer Lag
```text
Latest Offset - Consumed Offset
```
### Throughput
```text
Events/sec
```
### End-to-End Latency
```text
Event Created
      ↓
Dashboard Visible
```
### Watermark Lag
```text
Current Event Time
-
Watermark Time
```

## Streaming Machine Learning
Pipeline:
```text
Events
 ↓
Feature Calculation
 ↓
Feature Store
 ↓
Model
 ↓
Prediction
```

## Distributed Systems Theory
Topics:
- Consensus (leader election, failover)
- Replication (sync vs async)
- CAP Theorem
- Quorums
- Network Partitions
- Split Brain

## Advanced Kafka
- ISR (In-Sync Replicas)
- Leader Election
- KRaft (Kafka without ZooKeeper)
- Idempotent Producers
- Transactions
- Log Compaction
- Rebalancing
- Rack Awareness

## Streaming Design Patterns
### Fan-Out
```text
Event
 ↓
10 Consumers
```
### Event Enrichment
```text
Event
 ↓
Reference Data
 ↓
Enriched Event
```
### Dead Letter Queue
```text
Bad Event
 ↓
DLQ
```
### Saga Pattern
Distributed transactions.

## Cost Optimization
Questions:
- Why does state become expensive?
- Why do checkpoints slow down?
- Why does storage explode?
- Why does Kafka retention become costly?

## Stream Processing Anti-Patterns
### Giant Stateful Operators
```text
1 TB state
```
Recovery takes hours.

### Too Many Small Topics
```text
50,000 topics
```
Broker overhead explodes.

### Infinite Retention
Storage costs explode.

### Repartitioning Everything
Network bottlenecks appear.

---

# 16. Reprocessing & Replay

Critical topic.
Suppose:
```text
Bug found
```
in aggregation logic.
Need:
```text
Replay 90 days
```
of events.
Questions:
- Where do events come from?
- How do you avoid duplicates?
- Can state be rebuilt?

---

# 17. Out-of-Order Event Handling

A major production challenge.
Events arrive:
```text
Order Delivered
Order Shipped
Order Created
```
Questions:
- How do you reorder?
- How long do you wait?
- What if missing forever?
Patterns:
- buffering
- watermarking
- compensation events

---

# 18. Incremental Computation

The core idea behind stream processing.
Batch:
```text
Recompute everything
```
Streaming:
```text
Update only what changed
```

---

# Interview Preparation Roadmap

## Foundation
Events, Kafka, Partitions, Consumer Groups, Windows, Watermarks, State, Checkpointing

## Intermediate
CDC, Schema Evolution, Stream Joins, Exactly-Once, Backpressure, Observability

## Advanced
Flink Internals, Kafka Internals, Event Sourcing, Distributed Systems, Lakehouse Streaming

## Expert
Multi-region Streaming, Platform Architecture, Governance, Reliability, Cost Optimization

---

# Interview Questions

## Level 1: Core Concepts

**1. Event Time vs Processing Time**
A purchase event occurred at 10:00 AM but reached Kafka at 10:15 AM.
- What is the event time?
- What is the processing time?
- Which one should be used for hourly revenue calculations?
- Why?

**2. Late Data**
Suppose 5% of events arrive 30 minutes late.
How would you ensure hourly aggregates remain accurate?
Follow-up:
- How much lateness would you allow?
- What happens if data arrives after the window closes?

**3. Window Types**
You need to calculate:
- Revenue per hour
- Active users in last 15 minutes
- User browsing sessions
Which window type would you choose? Tumbling, Sliding, or Session? Why?

**4. Stateful vs Stateless**
Which of the following require state?
- Currency conversion
- Event filtering
- Running count
- Fraud detection
- Sessionization
Explain why.

**5. Exactly Once**
What does "exactly-once processing" actually mean?
Can it truly exist in a distributed system?
What assumptions must hold?

---

## Level 2: Kafka-Focused

**6. Partitioning Strategy**
You have 500M events/day. Events contain user_id, country, order_id.
What should be the Kafka partition key? user_id, order_id, or country?
Discuss pros and cons.

**7. Consumer Lag**
Your Kafka topic receives 100k events/sec. Consumers process 80k events/sec.
- What happens?
- How do you detect the issue?
- How do you fix it?

**8. Hot Partitions**
One customer generates 70% of traffic. Their user_id is used as partition key.
What problem occurs? How would you redesign partitioning?

**9. Offset Management**
Consumer processes event → Database write succeeds → Consumer crashes → Offset not committed.
Will data be duplicated? How would you prevent it?

**10. Kafka Retention**
Why might a company keep Kafka data for 1 day, 7 days, or 90 days? What are the tradeoffs?

---

## Level 3: Flink / Spark Streaming

**11. Watermark Design**
95% events arrive within 2 mins. 99% events arrive within 10 mins.
How would you choose watermark delay? Tradeoff between latency and accuracy.

**12. Checkpoint Recovery**
Flink job checkpoints every 5 mins. Crash occurs 4 mins after checkpoint.
- What happens during recovery?
- What data is replayed?
- Is duplication possible?

**13. Stream Join**
You have Orders Stream and Customers Stream. Customer updates can arrive after orders.
How would you handle missing customer data, delayed updates, and out-of-order arrivals?

**14. State Growth**
You maintain user sessions for 200 million users. State size keeps growing.
- Why?
- How do you prevent unbounded state growth?
- What is state TTL?

**15. Backpressure**
A downstream sink becomes slow. What happens in Flink?
How does backpressure propagate? How would you diagnose it?

---

## Level 4: Architecture Design

**16. Design Real-Time Fraud Detection**
Requirements: 50k transactions/sec, < 2 sec latency, 99.99% availability.
Design: ingestion layer, processing layer, state management, storage, recovery.
What technologies would you choose? Why?

**17. Real-Time Analytics Platform**
Design Uber Eats / Swiggy dashboard.
Need: orders per minute, revenue, city-level metrics, historical querying.
How would you combine Kafka, Flink, Iceberg, Trino?

**18. CDC Pipeline**
Database: Postgres. Need near real-time updates in lakehouse.
Design end-to-end architecture. Discuss Debezium, Kafka, Flink, Iceberg.

**19. Multi-Region Streaming**
Kafka cluster runs in Mumbai, Singapore, Frankfurt.
- How do you replicate?
- What if a region fails?
- How do you avoid duplicate processing?

**20. Real-Time Recommendation Engine**
User clicks Product A. Recommendation must update within 5 seconds.
Design the architecture. Explain event flow, feature computation, model serving, state management.

---

## Level 5: Failure & Distributed Systems

**21. Impossible Exactly-Once Scenario**
Kafka → Flink → External REST API. Flink sends request. API succeeds. Network fails before acknowledgement.
- Did request succeed?
- Should Flink retry?
- Can exactly-once still be guaranteed?

**22. Out-of-Order Events**
Events arrive: Order Created, Order Delivered, Order Shipped.
How would you reconstruct correct state?

**23. Deduplication at Scale**
You receive 10 billion events/day. Need deduplication.
How would you design state storage, expiration, and memory efficiency?

**24. CAP Theorem in Streaming**
How does CAP affect Kafka, Flink, and distributed state stores?
Which side is usually preferred?

**25. Consistency Tradeoff**
Business asks: Dashboard latency < 1 second. Current pipeline: 5 second watermark.
Would you reduce watermark, accept inaccuracies, or redesign architecture?
Explain the tradeoffs.

---

## Staff / Principal Level

**26. Why does stream processing exist if micro-batches work?**

**27. When should a company NOT use Kafka?**

**28. How would you migrate a batch warehouse into a streaming architecture?**

**29. How would you benchmark a stream processing system?**
Metrics: Throughput, End-to-end latency, Recovery time, Checkpoint duration, State size.

**30. Describe the hardest streaming production issue you've seen.**
Expected discussion: consumer lag, partition skew, checkpoint explosion, watermark issues, state corruption, duplicate events, replay storms.

---

## Further Reading

- [[Batch Processing]]
- [[Change Data Capture (CDC)]]
- [[Data Lake]]
- [[Distributed System]]
- [[Microservices]]
- [[Incremental Processing Interview Guide]]
