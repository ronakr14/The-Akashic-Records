The easiest way to understand it is:
> **Batch Processing = Process data later**
> **Stream Processing = Process data as it arrives**
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
# 4. Streaming Architecture
Basic architecture:
```text
Producer
   ↓
Message Broker
   ↓
Stream Processor
   ↓
Storage / Dashboard / Alerts
```
---
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
---
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
---
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
---
Streaming:
```text
Transaction happens
      ↓
Detect fraud immediately
      ↓
Block card
```
Good.
---
## Ride Sharing
```text
Driver location updates
Every few seconds
```
Need real-time processing.
Batch is useless.
---
## Stock Trading
Prices change every second.
Need instant reaction.
---
# 6. Core Streaming Concepts
Now we move beyond basics.
---
# Event Time vs Processing Time
Most beginners miss this.
Consider:
Event happened:
```text
10:00 AM
```
Arrived:
```text
10:05 AM
```
Processed:
```text
10:06 AM
```
Which time matters?
Usually:
```text
10:00 AM
```
because that's when it actually happened.
---
## Event Time
```text
Timestamp inside event
```
Example:
```json
{
 "timestamp":"10:00"
}
```
---
## Processing Time
```text
When processor sees event
```
Maybe:
```text
10:06
```
---
Real-world systems prefer:
```text
Event Time
```
because networks delay data.
---
# 7. Late Arriving Data
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
---
# 8. Windowing
Streams never end.
How do you calculate:
```text
Revenue per hour
```
if data never stops?
Use windows.
---
## Tumbling Window
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
---
```text
|---1 hr---|
|---1 hr---|
|---1 hr---|
```
---
## Sliding Window
Overlapping windows.
Example:
```text
Window = 10 mins
Slide = 1 min
```
Produces more granular metrics.
---
```text
0-10
1-11
2-12
3-13
```
---
## Session Window
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
---
# 9. Watermarks
One of the hardest concepts.
Problem:
```text
Events arrive late
```
How long should we wait?
Forever?
Impossible.
---
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
---
# 10. Stateful Processing
Simple processing:
```text
Event
 ↓
Transform
 ↓
Output
```
No memory.
Called:
```text
Stateless
```
---
Example:
```python
convert_currency(event)
```
---
Stateful processing remembers previous events.
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
---
Examples:
- running counts
- sessions
- fraud detection
- aggregates
---
# 11. Exactly Once Processing
Critical topic.
Imagine payment event:
```text
Purchase = ₹1000
```
Due to retry:
```text
same event processed twice
```
Result:
```text
₹2000 revenue
```
Wrong.
---
Possible guarantees:
## At Most Once
```text
May lose data
No duplicates
```
---
## At Least Once
```text
No data loss
Duplicates possible
```
Most common.
---
## Exactly Once
```text
No loss
No duplicates
```
Hardest.
Modern tools like Kafka + Flink support this.
---
# 12. Checkpointing
What if processor crashes?
Without checkpoint:
```text
Everything lost
```
---
Checkpoint:
```text
Save state periodically
```
Example:
```text
State = 1,000,000 events processed
```
Crash.
Restart.
Continue from checkpoint.
---
# 13. Stream Joins
Just like SQL joins.
Example:
Orders Stream:
```text
order_id
customer_id
```
Customer Stream:
```text
customer_id
name
```
Join:
```text
Order + Customer
```
Result:
```text
Order enriched with customer info
```
---
# 14. Stream vs Batch
|Feature|Batch|Streaming|
|---|---|---|
|Latency|Hours|Seconds/Milliseconds|
|Data|Historical|Continuous|
|Complexity|Lower|Higher|
|Cost|Lower|Higher|
|Real-time|No|Yes|
---
# 15. Typical Modern Data Engineering Streaming Stack
A common architecture:
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
# 16. What a Data Engineer Actually Does
In streaming projects, you'll typically:
### Ingestion
```text
App → Kafka
```
Design topics and schemas.
---
### Processing
```text
Kafka → Flink
```
Implement:
- aggregations
- joins
- deduplication
- enrichment
---
### Storage
```text
Flink → Iceberg
```
Store processed data.
---
### Monitoring
Track:
- lag
- throughput
- failures
- latency
---
# Mental Model
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
For a data engineer, the next logical topics are:
1. Kafka fundamentals (topics, partitions, offsets, consumer groups)
2. Stream processing with Flink
3. Event-driven architecture
4. CDC (Change Data Capture)
5. Lakehouse streaming (Iceberg + Kafka + Flink)
6. Real-time analytics architecture
These are the concepts that show up most often in modern data engineering interviews and production systems.
If you're interviewing for senior Data Engineer, Streaming Engineer, or Data Platform roles, the most interesting questions are rarely "What is Kafka?" They focus on tradeoffs, failure modes, scalability, correctness, and distributed systems behavior.
Here are progressively harder interview questions.
# Level 1: Core Concepts
### 1. Event Time vs Processing Time
A purchase event occurred at 10:00 AM but reached Kafka at 10:15 AM.
- What is the event time?
- What is the processing time?
- Which one should be used for hourly revenue calculations?
- Why?
---
### 2. Late Data
Suppose 5% of events arrive 30 minutes late.
How would you ensure hourly aggregates remain accurate?
Follow-up:
- How much lateness would you allow?
- What happens if data arrives after the window closes?
---
### 3. Window Types
You need to calculate:
- Revenue per hour
- Active users in last 15 minutes
- User browsing sessions
Which window type would you choose?
- Tumbling
- Sliding
- Session
Why?
---
### 4. Stateful vs Stateless
Which of the following require state?
- Currency conversion
- Event filtering
- Running count
- Fraud detection
- Sessionization
Explain why.
---
### 5. Exactly Once
What does "exactly-once processing" actually mean?
Can it truly exist in a distributed system?
What assumptions must hold?
---
# Level 2: Kafka-Focused
### 6. Partitioning Strategy
You have:
```text
500M events/day
```
Events contain:
```json
{
  "user_id": 123,
  "country": "IN",
  "order_id": 456
}
```
What should be the Kafka partition key?
- user_id
- order_id
- country
Discuss pros and cons.
---
### 7. Consumer Lag
Your Kafka topic receives:
```text
100k events/sec
```
Consumers process:
```text
80k events/sec
```
Questions:
- What happens?
- How do you detect the issue?
- How do you fix it?
---
### 8. Hot Partitions
One customer generates:
```text
70% of traffic
```
Their user_id is used as partition key.
What problem occurs?
How would you redesign partitioning?
---
### 9. Offset Management
What happens if:
```text
Consumer processes event
↓
Database write succeeds
↓
Consumer crashes
↓
Offset not committed
```
Will data be duplicated?
How would you prevent it?
---
### 10. Kafka Retention
Why might a company keep Kafka data for:
- 1 day
- 7 days
- 90 days
What are the tradeoffs?
---
# Level 3: Flink / Spark Streaming
### 11. Watermark Design
Suppose:
```text
95% events arrive within 2 mins
99% events arrive within 10 mins
```
How would you choose watermark delay?
Tradeoff between:
- latency
- accuracy
---
### 12. Checkpoint Recovery
Flink job:
```text
Checkpoint every 5 mins
```
Crash occurs:
```text
4 mins after checkpoint
```
Questions:
- What happens during recovery?
- What data is replayed?
- Is duplication possible?
---
### 13. Stream Join
You have:
```text
Orders Stream
```
and
```text
Customers Stream
```
Customer updates can arrive after orders.
How would you handle:
- missing customer data
- delayed customer updates
- out-of-order arrivals
---
### 14. State Growth
You maintain user sessions.
Users:
```text
200 million
```
State size keeps growing.
Questions:
- Why?
- How do you prevent unbounded state growth?
- What is state TTL?
---
### 15. Backpressure
A downstream sink becomes slow.
What happens in Flink?
How does backpressure propagate?
How would you diagnose it?
---
# Level 4: Architecture Design
### 16. Design Real-Time Fraud Detection
Requirements:
```text
50k transactions/sec
< 2 sec latency
99.99% availability
```
Design:
- ingestion layer
- processing layer
- state management
- storage
- recovery
What technologies would you choose?
Why?
---
### 17. Real-Time Analytics Platform
Design:
```text
Uber Eats / Swiggy dashboard
```
Need:
- orders per minute
- revenue
- city-level metrics
- historical querying
How would you combine:
- Kafka
- Flink
- Iceberg
- Trino
---
### 18. CDC Pipeline
Database:
```text
Postgres
```
Need near real-time updates in lakehouse.
Design end-to-end architecture.
Discuss:
- Debezium
- Kafka
- Flink
- Iceberg
---
### 19. Multi-Region Streaming
Kafka cluster runs in:
- Mumbai
- Singapore
- Frankfurt
Questions:
- How do you replicate?
- What if a region fails?
- How do you avoid duplicate processing?
---
### 20. Real-Time Recommendation Engine
User clicks:
```text
Product A
```
Recommendation must update within:
```text
5 seconds
```
Design the architecture.
Explain:
- event flow
- feature computation
- model serving
- state management
---
# Level 5: Failure & Distributed Systems
### 21. Impossible Exactly-Once Scenario
Suppose:
```text
Kafka → Flink → External REST API
```
Flink sends request.
API succeeds.
Network fails before acknowledgement.
Questions:
- Did request succeed?
- Should Flink retry?
- Can exactly-once still be guaranteed?
This exposes understanding of distributed systems limits.
---
### 22. Out-of-Order Events
Events arrive:
```text
Order Created
Order Delivered
Order Shipped
```
How would you reconstruct correct state?
---
### 23. Deduplication at Scale
You receive:
```text
10 billion events/day
```
Need deduplication.
How would you design:
- state storage
- expiration
- memory efficiency
---
### 24. CAP Theorem in Streaming
How does CAP affect:
- Kafka
- Flink
- Distributed state stores
Which side is usually preferred?
---
### 25. Consistency Tradeoff
Business asks:
```text
Dashboard latency < 1 second
```
Current pipeline:
```text
5 second watermark
```
Would you:
- reduce watermark?
- accept inaccuracies?
- redesign architecture?
Explain the tradeoffs.
---
# Questions Often Asked at Staff/Principal Level
### 26. Why does stream processing exist if micro-batches work?
---
### 27. When should a company NOT use Kafka?
---
### 28. How would you migrate a batch warehouse into a streaming architecture?
---
### 29. How would you benchmark a stream processing system?
Metrics?
- Throughput
- End-to-end latency
- Recovery time
- Checkpoint duration
- State size
---
### 30. Describe the hardest streaming production issue you've seen.
Expected discussion:
- consumer lag
- partition skew
- checkpoint explosion
- watermark issues
- state corruption
- duplicate events
- replay storms
---
A candidate who can deeply answer Questions 11–25 typically demonstrates senior-level streaming knowledge. Someone who can design and defend tradeoffs for Questions 16–30 is operating closer to Staff/Principal Data Engineer territory.
Yes. The topics we covered are the "mainstream" stream-processing concepts. However, modern streaming systems in production have several advanced areas that often separate a senior engineer from a staff/principal engineer.
# 1. Event-Driven Architecture (EDA)
Most streaming systems are actually event-driven systems.
Questions:
- What is an event?
- What is a command?
- What is a query?
- When should services communicate through events?
Example:
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
Interview question:
> When does event-driven architecture become a bad idea?
---
# 2. Change Data Capture (CDC)
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
Questions:
- Why CDC instead of batch extracts?
- How do you handle schema changes?
- How do you replay CDC history?
- How do deletes work?
Technologies:
- Debezium
- PostgreSQL
- MySQL
---
# 3. Stream Processing Internals
Many engineers know how to use Flink.
Few understand how it works.
Topics:
### Operator Chains
```text
Source
 ↓
Map
 ↓
Filter
 ↓
Aggregate
```
Questions:
- How are operators scheduled?
- How are records transferred?
---
### State Backend
Questions:
- Where is state stored?
- Memory?
- Disk?
- Remote storage?
For example:
- Apache Flink + RocksDB
---
### Incremental Checkpoints
Questions:
- Why are full checkpoints expensive?
- How do incremental checkpoints work?
---
# 4. Data Contracts & Schema Evolution
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
---
# 5. Lakehouse Streaming
This is where data engineering is moving.
Architecture:
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
Questions:
- How does streaming data get committed?
- How are snapshots maintained?
- How does time travel work?
- How does compaction work?
Technologies:
- Apache Iceberg
- Apache Hudi
- Delta Lake
---
# 6. Data Quality in Streaming
Batch quality checks are easier.
Streaming introduces new challenges.
Questions:
- How do you detect duplicates?
- Missing events?
- Out-of-order events?
- Corrupt events?
Example:
```text
Expected:
1000 events/minute
Received:
10 events/minute
```
How do you alert?
---
# 7. Stream Governance
Large organizations struggle here.
Questions:
- Who owns topics?
- How long are events retained?
- Can events be deleted?
- Who can publish?
Topics:
- PII masking
- GDPR compliance
- Data lineage
- Auditing
---
# 8. Streaming Observability
A huge production topic.
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
Interview question:
> A dashboard is 20 minutes behind. Where do you start investigating?
---
# 9. Streaming Machine Learning
Growing area.
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
Questions:
- Online features vs offline features?
- Feature freshness?
- Model drift?
Tools:
- Feast
- Apache Kafka
---
# 10. Distributed Systems Theory
This is the foundation beneath everything.
Topics:
### Consensus
- Leader election
- Failover
### Replication
- Sync replication
- Async replication
### CAP Theorem
### Quorums
### Network Partitions
### Split Brain
Interview question:
> What happens if Kafka brokers lose connectivity with each other?
---
# 11. Advanced Kafka
Most interviews stop at producers and consumers.
Senior interviews continue into:
### ISR
In-Sync Replicas
### Leader Election
### KRaft
Kafka without ZooKeeper
### Idempotent Producers
### Transactions
### Log Compaction
### Rebalancing
### Rack Awareness
---
# 12. Streaming Design Patterns
These appear repeatedly in real systems.
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
---
# 13. Cost Optimization
Rarely discussed but highly important.
Questions:
- Why does state become expensive?
- Why do checkpoints slow down?
- Why does storage explode?
- Why does Kafka retention become costly?
Production reality:
```text
Throughput problem
      ↓
More servers
      ↓
Higher cost
```
Staff engineers often optimize architecture instead of simply scaling.
---
# 14. Stream Processing Anti-Patterns
These are excellent interview topics.
Examples:
### Giant Stateful Operators
```text
1 TB state
```
Recovery takes hours.
---
### Too Many Small Topics
```text
50,000 topics
```
Broker overhead explodes.
---
### Infinite Retention
Storage costs explode.
---
### Repartitioning Everything
Network bottlenecks appear.
---
# Mastery Roadmap
If your goal is deep expertise, I'd rank topics like this:
### Foundation
1. Events
2. Kafka
3. Partitions
4. Consumer groups
5. Windows
6. Watermarks
7. State
8. Checkpointing
### Intermediate
9. CDC
10. Schema evolution
11. Stream joins
12. Exactly-once
13. Backpressure
14. Observability
### Advanced
15. Flink internals
16. Kafka internals
17. Event sourcing
18. Distributed systems
19. Lakehouse streaming
20. Cost optimization
### Expert
21. Multi-region streaming
22. Large-scale state management
23. Real-time ML systems
24. Streaming platform architecture
25. Streaming governance and reliability
At that point, you're no longer just "using Kafka/Flink"—you're designing and operating streaming platforms that other engineering teams build on. That's where principal-level discussions usually happen.
If we narrow the scope to **stream data processing itself** (and exclude adjacent topics like Kafka internals, CDC, governance, ML, and distributed systems), there are still some advanced stream-processing concepts that are often overlooked.
These are the topics that separate someone who can _use_ Flink/Spark Streaming from someone who truly understands stream processing.
---
# 1. Event-Time Processing Deep Dive
Most engineers know:
- Event Time
- Processing Time
- Watermarks
But few understand the edge cases.
### Topics
- Idle partitions
- Watermark propagation
- Watermark alignment
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
Understanding this is critical for large-scale streaming jobs.
---
# 2. Advanced Windowing
Most people stop at:
- Tumbling
- Sliding
- Session
There are more concepts.
### Custom Windows
Example:
```text
Market Open → Market Close
```
instead of fixed hours.
---
### Dynamic Windows
Window size changes based on business logic.
Example:
```text
VIP Users → 1 minute window
Normal Users → 30 minute window
```
---
### Window Triggers
Instead of waiting for window completion.
Trigger early:
```text
Every 10 seconds
```
while the window remains open.
---
### Window Eviction
Remove old records before final aggregation.
Useful for memory optimization.
---
# 3. Stateful Processing Internals
State is the heart of stream processing.
### Keyed State
```text
User A → state
User B → state
User C → state
```
Each key owns its own state.
---
### Operator State
Shared state across operator instances.
---
### Broadcast State
Used for:
```text
Rules
Configurations
Reference Data
```
Example:
```text
Fraud Rules Stream
```
updates all processors dynamically.
---
# 4. State Lifecycle Management
One of the most important production topics.
### State TTL
Automatically remove old state.
Example:
```text
User inactive for 30 days
```
Delete state.
---
### State Cleanup
Questions:
- When does cleanup happen?
- During checkpoint?
- During access?
---
### State Migration
What happens when:
```text
Job upgraded
```
but state already exists?
---
# 5. Stream Joins Deep Dive
Most engineers know stream-to-stream joins.
There are multiple types.
---
### Stream-Stream Join
```text
Orders
JOIN
Payments
```
---
### Stream-Table Join
```text
Orders Stream
JOIN
Customer Table
```
---
### Temporal Join
Join using historical version.
Example:
```text
Customer Tier
```
at the time order was placed.
Not current value.
---
### Interval Join
Join only within time bounds.
Example:
```text
Order
Payment
within 10 minutes
```
---
# 6. Out-of-Order Event Handling
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
# 7. Reprocessing & Replay
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
# 8. Time Semantics
Often skipped.
---
### Processing Time
Fastest.
Less accurate.
---
### Event Time
Accurate.
More complex.
---
### Ingestion Time
Middle ground.
Time assigned when entering system.
Questions:
- When should each be used?
---
# 9. Stream Processing Guarantees
Much deeper than:
- At-most-once
- At-least-once
- Exactly-once
Topics:
### Deterministic Processing
Can results be reproduced?
---
### Idempotency
Can duplicate events be safely processed?
---
### Transactional Sinks
Can state and output commit atomically?
---
# 10. Scaling Stateful Operators
One of the hardest areas.
Suppose:
```text
500 million users
```
Each user maintains state.
Questions:
- How is state partitioned?
- What happens when scaling from:
```text
8 → 64 workers
```
- How is state redistributed?
This introduces:
- rescaling
- repartitioning
- state redistribution
---
# 11. Backpressure Mechanics
Many engineers can define it.
Few can explain it.
Example:
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
Questions:
- What happens upstream?
- How do queues fill?
- How is throughput affected?
---
# 12. Fault Tolerance Algorithms
Beyond checkpointing.
Topics:
### Barrier Alignment
Core Flink concept.
Used for consistent checkpoints.
Questions:
- Why are barriers needed?
- How do barriers move through topology?
---
### Unaligned Checkpoints
Introduced to solve severe backpressure issues.
---
### Savepoints
Different from checkpoints.
Used for:
```text
Job upgrades
Migration
```
---
# 13. Processing Graph Optimization
Execution graph concepts.
Questions:
- Operator chaining
- Task slots
- Parallelism
- Network shuffle
Example:
```text
Map
Filter
Aggregate
```
Can be fused into fewer tasks.
---
# 14. Streaming SQL
Increasingly important.
Examples:
```sql
SELECT
    user_id,
    COUNT(*)
FROM orders
GROUP BY
    user_id,
    TUMBLE(order_time, INTERVAL '1' HOUR)
```
Topics:
- Window aggregations
- Temporal joins
- Streaming materialized views
- Incremental computation
---
# 15. Incremental Computation
The core idea behind stream processing.
Batch:
```text
Recompute everything
```
Streaming:
```text
Update only what changed
```
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
# The Last 5% Most Engineers Never Learn
These are genuinely expert-level stream-processing topics:
1. Watermark alignment across partitions
2. Barrier alignment algorithms
3. Incremental checkpoint internals
4. State redistribution during rescaling
5. Temporal joins and versioned tables
6. Deterministic replay
7. Event-time correctness proofs
8. Stateful operator optimization
9. Incremental view maintenance
10. Streaming query planners
Once you understand those, you're essentially studying stream processing as a distributed systems discipline rather than as a Kafka/Flink user. That's the deepest layer of the subject.