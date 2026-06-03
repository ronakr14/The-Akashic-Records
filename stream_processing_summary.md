# Stream Data Processing -- Condensed Study Guide

## Foundations

-   Streams = continuous flow of events.
-   Event = something that happened (purchase, login, sensor reading).
-   Streaming processes data as it arrives; batch processes data later.

## Core Architecture

Producer → Broker (Kafka) → Stream Processor (Flink/Spark) →
Storage/Analytics

## Essential Concepts

### Time

-   Event Time: when event actually happened.
-   Processing Time: when system processed it.
-   Ingestion Time: when event entered the platform.

### Windowing

-   Tumbling: fixed non-overlapping windows.
-   Sliding: overlapping windows.
-   Session: activity separated by inactivity.
-   Advanced: custom, dynamic, triggered windows.

### Watermarks

-   Estimate completeness of event-time data.
-   Handle late-arriving events.
-   Advanced: watermark propagation, alignment, skew, idle partitions.

### State

-   Stateless: transform/filter only.
-   Stateful: counts, aggregations, sessions, fraud detection.
-   Types:
    -   Keyed State
    -   Operator State
    -   Broadcast State
-   State management:
    -   TTL
    -   Cleanup
    -   Migration

## Processing Guarantees

-   At-most-once
-   At-least-once
-   Exactly-once
-   Idempotency
-   Deterministic processing
-   Transactional sinks

## Fault Tolerance

-   Checkpoints
-   Incremental checkpoints
-   Savepoints
-   Barrier alignment
-   Unaligned checkpoints
-   Recovery and replay

## Stream Joins

-   Stream-Stream
-   Stream-Table
-   Temporal joins
-   Interval joins

## Scaling Challenges

-   State redistribution during rescaling
-   Hot keys and partition skew
-   Backpressure propagation
-   Large-state management

## Reprocessing

-   Replay historical events
-   Rebuild state
-   Correct bugs without data loss

## Streaming SQL

-   Window aggregations
-   Temporal joins
-   Materialized views
-   Incremental computation

## Most Important Mental Model

Batch: - Recompute everything.

Streaming: - Update only what changed.

## Advanced Topics

1.  Watermark alignment
2.  Barrier alignment algorithms
3.  Incremental checkpoint internals
4.  Stateful operator optimization
5.  Deterministic replay
6.  Incremental view maintenance
7.  Streaming query planners
8.  Event-time correctness
9.  Large-scale state management
10. Temporal/versioned tables

## Interview Preparation Roadmap

### Foundation

Events, Kafka, Partitions, Consumer Groups, Windows, Watermarks, State,
Checkpointing

### Intermediate

CDC, Schema Evolution, Stream Joins, Exactly-Once, Backpressure,
Observability

### Advanced

Flink Internals, Kafka Internals, Event Sourcing, Distributed Systems,
Lakehouse Streaming

### Expert

Multi-region Streaming, Platform Architecture, Governance, Reliability,
Cost Optimization
