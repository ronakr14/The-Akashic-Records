```table-of-contents
```

# Microservices — Interview Questions

## Architecture & Service Boundaries

**1. You have a monolithic e-commerce application. How would you identify microservice boundaries?**

Expected discussion: bounded contexts from [[DDD]], team ownership ([[Conway's Law]]), data cohesion, communication patterns. What metrics would you use? How do you avoid creating distributed monoliths? When should two services remain together?

**2. How do you decide whether functionality belongs in an existing service or a new service?**

Expected discussion: domain ownership, coupling, cohesion, Conway's Law, team ownership.

**3. What are the signs that a microservice should be split?**

Expected discussion: multiple teams stepping on each other, conflicting requirements, different scaling needs, independent deployability suffering.

**4. What are the signs that multiple microservices should be merged?**

Many engineers only know how to split systems. Expected discussion: tight coupling, coordinated deployments always needed, same team owns both, excessive network chatter for simple operations.

**5. Design a microservice architecture for a ride-sharing platform.**

Expect discussion around: User Service, Driver Service, Matching Service, Pricing Service, Payment Service, Location Service. Then explain communication patterns.

## Data Ownership

**6. Why should each microservice own its database?**

What problems occur with 10 services sharing 1 database? (Answer: schema coupling, no clear ownership, cascading failures, distributed monolith.)

**7. Two services need the same data. How would you avoid direct database access?**

Possible approaches: APIs, event propagation, CQRS, materialized views.

**8. How would you handle schema evolution across services?**

Scenario: User Service changes customer schema, 20 services consume it. Expected: versioned APIs, backward compatibility, event schema registries.

**9. How do you prevent data duplication from becoming inconsistent?**

Expected: event-driven updates, eventual consistency model, reconciliation jobs.

**10. How would you implement data lineage across hundreds of services?**

Interesting for data engineering roles. Expected: event metadata, trace IDs propagated through the call chain, centralized catalog.

## Service Communication

**11. When would you choose REST versus [[gRPC]]?**

Expected: REST for public APIs, browser-facing, human-readable. gRPC for internal service-to-service, performance-critical, polyglot environments.

**12. When would you choose synchronous versus asynchronous communication?**

Expected tradeoffs: latency, availability, consistency, coupling.

**13. A service call takes 50ms today but 2 seconds tomorrow. What happens to downstream services?**

Expected: resource exhaustion, cascading failures. Solutions: timeouts, circuit breakers, bulkheads.

**14. How do cascading failures occur?**

Draw: `A → B → C → D`. D fails. What happens next? Expected: retry storms, thread pool exhaustion, cascading timeouts.

**15. How would you design service communication for 10,000 requests per second?**

Expected: async messaging, connection pooling, load balancing, back-pressure.

## Distributed Transactions

**16. Customer charged successfully but order creation failed. How would you recover?**

Expected: compensating transaction, Saga pattern, retry with idempotency keys.

**17. Explain the [[Saga Pattern]].**

Then ask: What happens if compensation fails? Expected: manual intervention, retry compensation, alert for human review.

**18. Why are distributed transactions difficult?**

Expected discussion: [[CAP Theorem]], network failures, partial success.

**19. Would you use two-phase commit in production?**

Why or why not? Expected: 2PC is blocking and fragile under network partitions. Prefer Saga or eventual consistency.

**20. Design a payment workflow that guarantees no double charging.**

Expected: idempotency keys, deduplication at the payment service, deterministic transaction IDs.

## Reliability & Resilience

**21. Design a system that continues operating when 30% of services are unavailable.**

Expected: graceful degradation, circuit breakers, fallback responses, bulkheads.

**22. What is a circuit breaker?**

Follow-up: How do you tune thresholds? Expected: error rate threshold, half-open state, request probing.

**23. What is the difference between Retry, Timeout, Circuit Breaker, and Bulkhead?**

Each addresses a different failure mode. Retry handles transient failures. Timeout prevents waiting forever. Circuit Breaker prevents repeated calls to a failing service. Bulkhead isolates resources.

**24. A dependency becomes extremely slow but never completely fails. How do you detect it?**

Expected: latency monitoring, percentile tracking (p99), timeouts.

**25. How would you implement graceful degradation?**

Example: Recommendation Service down. Should checkout still work? Yes — serve cached recommendations or skip the feature entirely.

## Event-Driven Architecture

**26. Explain event-driven microservices.**

Expected: events as the communication mechanism, loose coupling, async processing.

**27. What problems can event-driven systems introduce?**

Expected: duplication, ordering, replay, debugging.

**28. What is the difference between an event and a command?**

Event: something happened (past tense). Command: request to do something (imperative). Events are facts; commands are intentions.

**29. How would you guarantee event delivery?**

Expected: at-least-once delivery with idempotent consumers, producer retries, dead-letter queues.

**30. What is exactly-once processing? Does it really exist?**

Great senior-level answer: true exactly-once is extremely hard. Practical approach: at-least-once delivery + idempotent processing = effectively exactly-once.

## Message Queues & Kafka

**31. Explain how a [[Apache Kafka]]-based microservice architecture works.**

Expected: topics, partitions, consumer groups, brokers, offset management.

**32. What happens when consumers lag behind producers?**

Expected: increased latency, potential data loss if retention period expires, need to scale consumers.

**33. How would you handle out-of-order events?**

Expected: partition-level ordering, event timestamps, sequence IDs, reorder buffers.

**34. How do you design idempotent consumers?**

Expected: deduplication by event ID, database unique constraints, idempotent write operations.

**35. A topic suddenly receives 100x traffic. What happens?**

Expected: partition scaling, consumer auto-scaling, back-pressure on producers, potential need to add brokers.

## Observability

**36. A user reports "Checkout is slow." There are 150 services. How do you find the root cause?**

Expected: distributed tracing, look for the span with highest latency, drill into that service's dependencies.

**37. What telemetry would you collect from every microservice?**

Expected: latency, throughput, error rate, resource utilization (CPU, memory).

**38. Explain distributed tracing.**

Expected: trace context propagation (trace ID, parent span ID), sampling, tools like [[OpenTelemetry]] and [[Jaeger]].

**39. How would you correlate logs across services?**

Expected: trace ID in every log line, structured logging, centralized aggregation.

**40. What would your service health dashboard contain?**

Expected: error rate, latency percentiles, throughput, saturation metrics, dependency health.

## Scalability

**41. One service receives 100x more traffic than all others. How do you scale it?**

Expected: horizontal scaling, dedicated resource pool, caching, consider if it should be split further.

**42. How do you identify bottlenecks in a microservice ecosystem?**

Expected: tracing data, metrics analysis, load testing, identify the service with highest latency or error rate.

**43. Explain horizontal versus vertical scaling.**

Horizontal: add more instances. Vertical: bigger instances. Microservices favor horizontal.

**44. Design a service capable of handling one million requests per second.**

Expected: stateless design, caching, CDN, horizontal scaling, load balancing, async processing.

**45. How would you estimate infrastructure cost before deployment?**

Expected: load testing, resource profiling, traffic modeling, cost calculators.

## Kubernetes & Containers

**46. Why are microservices commonly deployed on containers?**

Using [[Docker]]: lightweight, portable, consistent environments, resource isolation.

**47. How does [[Kubernetes]] help microservices?**

Expected: orchestration, auto-scaling, service discovery, load balancing, self-healing, rolling updates.

**48. A pod continuously crashes. How would you investigate?**

Expected: check logs, resource limits, liveness probes, events, recent deployments.

**49. How would you perform a zero-downtime deployment?**

Expected: rolling updates, readiness probes, graceful shutdown, connection draining.

**50. What deployment strategies do you know?**

Expected: Blue-Green, Canary, Rolling, Shadow.

## Security

**51. How do services authenticate each other?**

Expected: [[mTLS]], service accounts, API keys, JWT tokens.

**52. How do you secure service-to-service communication?**

Expected: TLS, mTLS, certificates, network policies.

**53. Design authentication and authorization for 500 microservices.**

Expected: centralized identity provider, JWT with claims, service-level authorization, API gateway for token validation.

**54. How would you manage secrets?**

Expected: secret management tools (Vault, Kubernetes Secrets), never in code or environment variables.

**55. How do you rotate credentials without downtime?**

Expected: dual credentials, automated rotation, short-lived tokens.

## Failure Scenarios

**56. Payment Service is healthy but responds after 10 seconds. What happens to the platform?**

Expected: thread pool exhaustion, cascading failures. Mitigation: timeouts, circuit breakers, bulkheads.

**57. One service starts producing corrupted events. How do you contain the blast radius?**

Expected: event validation, dead-letter queues, consumer-side validation, circuit breaker on event processing.

**58. Network latency between regions increases by 20x. How does the architecture behave?**

Expected: timeouts trigger, circuit breakers open, async communication becomes critical, consider multi-region deployment.

**59. Database replication falls behind by 1 hour. What failures might users see?**

Expected: stale reads, inconsistency between write and read replicas, user confusion.

**60. A Kafka cluster becomes unavailable during peak traffic. Walk through incident response.**

Expected: identify impact, switch to retry/dead-letter, communicate status, recover from offsets after restoration.

## Staff/Principal-Level Questions

**61. When are microservices the wrong architectural choice?**

Expected: small teams, unclear domain boundaries, when operational complexity outweighs benefits.

**62. How would you identify a distributed monolith?**

Symptoms: shared database, synchronous chains, coordinated deployments.

**63. Your company has 500 microservices. How would you reduce operational complexity?**

Expected: consolidate where appropriate, platform engineering, standardized tooling, service mesh.

**64. How would you measure microservice architecture success?**

Metrics: deployment frequency, MTTR, lead time, availability.

**65. If you were redesigning microservices from scratch today, what would you do differently?**

This question reveals architectural maturity. Expected: start with monolith, extract services at boundaries, invest in platform early, avoid over-fragmentation.

## Staff/Principal Deep Dive

**66. Design a global order-processing platform.**

Requirements: 100 million orders/day, 50 countries, multi-region, 99.99% availability, no double charging, event-driven, real-time inventory.

Discuss: service boundaries, event design, consistency model, failure handling, scaling strategy, observability, disaster recovery, cost optimization.

A strong answer touches almost every major microservices concept: domain design, messaging, distributed transactions, resiliency, scalability, and operations.

## See Also
- [[Microservice]] — microservice architecture principles
- [[Monolithic System]] — when monoliths win
- [[Distributed System]] — distributed systems foundations
- [[Idempotency]] — idempotency in service communication
- [[Partitioning 1]] — data partitioning in microservices
