Perfect follow-up after monoliths.

A common learning path is:

**Monolith → Problems at Scale → Microservices → Distributed Systems**

Let's build intuition first before discussing architecture diagrams and buzzwords.

---

# What Is a Microservice?

Imagine you're running a restaurant.

In a monolith, one giant kitchen does everything:

- Takes orders
    
- Cooks food
    
- Handles billing
    
- Manages inventory
    
- Tracks deliveries
    

Everything is in one place.

Now imagine the restaurant grows enormously.

Instead of one giant kitchen, you create specialized teams:

- Pizza kitchen
    
- Dessert kitchen
    
- Billing counter
    
- Delivery department
    
- Inventory department
    

Each team works independently.

That's essentially a microservice architecture.

A microservice is:

> A small, independent application responsible for one business capability.

Examples:

|Service|Responsibility|
|---|---|
|User Service|User accounts|
|Order Service|Orders|
|Payment Service|Payments|
|Inventory Service|Stock|
|Notification Service|Email/SMS|

Each service owns its own logic.

---

# Why Did Microservices Become Popular?

Monoliths work well initially.

Problems appear when:

- Codebase becomes huge
    
- Hundreds of developers work together
    
- Deployments become risky
    
- Scaling requirements differ
    

Example:

You have:

- User module
    
- Payment module
    
- Reporting module
    

Reporting becomes extremely busy.

With a monolith:

```text
Scale entire application
```

Even though only reporting needs more resources.

With microservices:

```text
Scale Reporting Service only
```

Much cheaper.

---

# High-Level Architecture

A simple e-commerce system:

```text
Customer
    |
    v
API Gateway
    |
---------------------------------
|       |        |        |
User   Order   Payment  Product
Svc    Svc     Svc      Svc
```

Each box is a separate application.

---

# Core Principle

Microservices are organized around:

### Business Capabilities

Not:

```text
Database Team
UI Team
API Team
```

Instead:

```text
Order Team
Payment Team
Customer Team
```

Each team owns everything for that domain.

This is called:

Domain-Driven Design (DDD)

---

# Service Independence

Each service should be able to:

- Develop independently
    
- Deploy independently
    
- Scale independently
    

Example:

Order Service:

```text
Version 1 deployed
```

Payment Service:

```text
Version 2 deployed
```

No need to deploy everything together.

---

# Database Ownership

One of the biggest differences from monoliths.

Monolith:

```text
One shared database
```

```text
Orders Table
Users Table
Payments Table
```

Microservices:

```text
Order Service -> Order DB

Payment Service -> Payment DB

User Service -> User DB
```

Each service owns its data.

---

# Why Separate Databases?

Without separation:

```text
Payment Service directly modifies Orders table
```

Chaos begins.

Nobody knows who changed what.

Ownership becomes unclear.

Microservices enforce:

```text
Only Order Service can modify order data.
```

---

# Service Communication

Since services are separate, they must talk to each other.

Two approaches:

## 1. Synchronous Communication

Like a phone call.

```text
Order Service
      |
      v
Payment Service
```

Order waits for Payment response.

Usually:

- HTTP
    
- REST
    
- gRPC
    

Example:

```text
Create Order
   |
Charge Card
   |
Success
```

---

## 2. Asynchronous Communication

Like sending an email.

```text
Order Service
     |
     v
Message Queue
     |
     v
Payment Service
```

Order doesn't wait.

Processes continue later.

Usually:

- Apache Kafka
    
- RabbitMQ
    
- Apache Pulsar
    

---

# Event-Driven Architecture

A common microservices pattern.

Order created:

```text
OrderCreated Event
```

Published to broker.

Other services subscribe:

```text
Inventory Service
Notification Service
Analytics Service
```

All react independently.

```text
Order Created
      |
      +--> Inventory Updated
      +--> Email Sent
      +--> Analytics Updated
```

Very scalable.

---

# API Gateway

Users should not call 50 services directly.

Instead:

```text
Client
   |
API Gateway
   |
Many Services
```

Gateway handles:

- Routing
    
- Authentication
    
- Rate limiting
    
- Logging
    

Popular examples:

- Kong
    
- NGINX
    
- Spring Cloud Gateway
    

---

# Service Discovery

Question:

How does Order Service know where Payment Service runs?

Servers change constantly.

Solution:

Service Registry.

```text
Payment Service
   |
Registers itself
   |
Service Registry
```

Order asks:

```text
Where is Payment Service?
```

Registry answers.

Examples:

- Consul
    
- Eureka
    

---

# Fault Tolerance

Microservices assume failures happen.

Example:

```text
Payment Service Down
```

Should entire website crash?

No.

Use:

### Retry

```text
Try again
```

### Timeout

```text
Wait 2 seconds
Stop waiting
```

### Circuit Breaker

```text
Payment failing repeatedly
```

Temporarily stop sending requests.

Prevents cascading failures.

---

# Distributed Transactions Problem

One of the hardest topics.

Suppose:

```text
Create Order
Charge Card
Update Inventory
```

Order succeeds.

Payment succeeds.

Inventory fails.

Now what?

You have:

```text
Customer charged
No inventory reserved
```

Bad state.

---

# Saga Pattern

Microservices often use:

Saga Pattern

Instead of one giant transaction.

```text
Step 1: Create Order
Step 2: Charge Card
Step 3: Reserve Inventory
```

If step 3 fails:

```text
Refund Payment
Cancel Order
```

Compensating actions restore consistency.

---

# Observability

Debugging monolith:

```text
One log file
```

Debugging microservices:

```text
100 services
500 containers
Thousands of requests
```

Need observability.

Three pillars:

## Logs

What happened?

```text
Order created
Payment failed
```

---

## Metrics

How healthy?

```text
CPU
Memory
Latency
Errors
```

---

## Traces

Request journey.

```text
API Gateway
   |
Order Service
   |
Payment Service
   |
Inventory Service
```

Trace follows the request.

Popular tools:

- Prometheus
    
- Grafana
    
- Jaeger
    
- OpenTelemetry
    

---

# Deployment with Containers

Microservices are usually packaged as containers.

```text
User Service Container
Order Service Container
Payment Service Container
```

Container technology:

Docker

---

# Orchestration

Running 500 containers manually is impossible.

Need orchestration.

Most companies use:

Kubernetes

Responsibilities:

- Scheduling
    
- Scaling
    
- Recovery
    
- Networking
    
- Rolling updates
    

---

# Advantages

### Faster Development

Teams work independently.

### Independent Deployments

No giant release.

### Independent Scaling

Scale only busy services.

### Technology Flexibility

Order:

```text
Java
```

Analytics:

```text
Python
```

Payments:

```text
Go
```

Possible because services are separate.

---

# Disadvantages

This is where many beginners get surprised.

Microservices solve monolith problems by introducing distributed systems problems.

You trade:

```text
Code complexity
```

for

```text
Operational complexity
```

New challenges:

- Network failures
    
- Service discovery
    
- Data consistency
    
- Distributed transactions
    
- Monitoring
    
- Security
    
- Debugging
    

---

# When NOT to Use Microservices

Many startups make this mistake.

Team size:

```text
3 developers
```

Architecture:

```text
50 microservices
```

Result:

```text
50 small headaches
```

For small teams:

```text
Start with a monolith
```

Often the best decision.

Even companies like Amazon, Netflix, and Uber evolved toward microservices after reaching significant scale, not on day one.

---

# Mental Model

Think of it this way:

### Monolith

```text
One large factory
```

Simple to manage.

Hard to scale selectively.

---

### Microservices

```text
Many specialized factories
```

Easy to scale individually.

Harder to coordinate.

---

### Distributed System

```text
Entire city of factories
```

Now networking, communication, failures, and coordination become the primary challenges.

That's why microservices are really an application of distributed systems. Once you understand microservices, the next logical step is learning distributed systems concepts such as consistency, partitioning, replication, consensus, messaging, and fault tolerance. Those ideas explain why large-scale microservice systems behave the way they do.

If you're interviewing for a **Senior Data Engineer, Platform Engineer, Backend Engineer, Staff Engineer, or Distributed Systems role**, interviewers often use microservices questions to test whether you understand the realities of operating distributed systems—not whether you can draw boxes on a whiteboard.

Here are some challenging, scenario-based questions.

---

# Architecture & Service Boundaries

### 1. You have a monolithic e-commerce application. How would you identify microservice boundaries?

Follow-ups:

- What metrics would you use?
    
- How do you avoid creating distributed monoliths?
    
- When should two services remain together?
    

---

### 2. How do you decide whether functionality belongs in an existing service or a new service?

Expected discussion:

- Domain ownership
    
- Coupling
    
- Cohesion
    
- Conway's Law
    
- Team ownership
    

---

### 3. What are the signs that a microservice should be split?

---

### 4. What are the signs that multiple microservices should be merged?

Many engineers only know how to split systems.

---

### 5. Design a microservice architecture for a ride-sharing platform.

Expect discussion around:

- User Service
    
- Driver Service
    
- Matching Service
    
- Pricing Service
    
- Payment Service
    
- Location Service
    

Then explain communication patterns.

---

# Data Ownership

### 6. Why should each microservice own its database?

What problems occur with:

```text
10 services
1 shared database
```

---

### 7. Two services need the same data. How would you avoid direct database access?

Possible approaches:

- APIs
    
- Event propagation
    
- CQRS
    
- Materialized views
    

---

### 8. How would you handle schema evolution across services?

Scenario:

```text
User Service changes customer schema
20 services consume it
```

---

### 9. How do you prevent data duplication from becoming inconsistent?

---

### 10. How would you implement data lineage across hundreds of services?

Interesting for data engineering roles.

---

# Service Communication

### 11. When would you choose REST versus gRPC?

---

### 12. When would you choose synchronous communication versus asynchronous communication?

Expected tradeoffs:

- Latency
    
- Availability
    
- Consistency
    
- Coupling
    

---

### 13. A service call takes 50ms today but 2 seconds tomorrow. What happens to downstream services?

---

### 14. How do cascading failures occur?

Draw:

```text
A -> B -> C -> D
```

D fails.

What happens next?

---

### 15. How would you design service communication for 10,000 requests per second?

---

# Distributed Transactions

### 16. Customer charged successfully but order creation failed.

How would you recover?

---

### 17. Explain the Saga pattern.

Then ask:

```text
What happens if compensation fails?
```

---

### 18. Why are distributed transactions difficult?

Expected discussion:

- CAP theorem
    
- Network failures
    
- Partial success
    

---

### 19. Would you use two-phase commit in production?

Why or why not?

---

### 20. Design a payment workflow that guarantees no double charging.

---

# Reliability & Resilience

### 21. Design a system that continues operating when 30% of services are unavailable.

---

### 22. What is a circuit breaker?

Follow-up:

How do you tune thresholds?

---

### 23. What is the difference between:

- Retry
    
- Timeout
    
- Circuit breaker
    
- Bulkhead
    

---

### 24. A dependency becomes extremely slow but never completely fails.

How do you detect it?

---

### 25. How would you implement graceful degradation?

Example:

```text
Recommendation Service down
```

Should checkout still work?

---

# Event-Driven Architecture

### 26. Explain event-driven microservices.

---

### 27. What problems can event-driven systems introduce?

Expected:

- Duplication
    
- Ordering
    
- Replay
    
- Debugging
    

---

### 28. What is the difference between an event and a command?

---

### 29. How would you guarantee event delivery?

---

### 30. What is exactly-once processing?

Then ask:

```text
Does it really exist?
```

Great senior-level question.

---

# Message Queues & Kafka

### 31. Explain how a Kafka-based microservice architecture works.

Using:

Apache Kafka

---

### 32. What happens when consumers lag behind producers?

---

### 33. How would you handle out-of-order events?

---

### 34. How do you design idempotent consumers?

---

### 35. A topic suddenly receives 100x traffic.

What happens?

---

# Observability

### 36. A user reports:

```text
Checkout is slow
```

There are:

```text
150 services
```

How do you find the root cause?

---

### 37. What telemetry would you collect from every microservice?

Expected:

- Latency
    
- Throughput
    
- Error rate
    
- Resource utilization
    

---

### 38. Explain distributed tracing.

Tools often include:

- OpenTelemetry
    
- Jaeger
    

---

### 39. How would you correlate logs across services?

---

### 40. What would your service health dashboard contain?

---

# Scalability

### 41. One service receives 100x more traffic than all others.

How do you scale it?

---

### 42. How do you identify bottlenecks in a microservice ecosystem?

---

### 43. Explain horizontal versus vertical scaling.

---

### 44. Design a service capable of handling one million requests per second.

---

### 45. How would you estimate infrastructure cost before deployment?

---

# Kubernetes & Containers

### 46. Why are microservices commonly deployed on containers?

Using:

Docker

---

### 47. How does Kubernetes help microservices?

Using:

Kubernetes

---

### 48. A pod continuously crashes.

How would you investigate?

---

### 49. How would you perform a zero-downtime deployment?

---

### 50. What deployment strategies do you know?

Expected:

- Blue-Green
    
- Canary
    
- Rolling
    
- Shadow
    

---

# Security

### 51. How do services authenticate each other?

---

### 52. How do you secure service-to-service communication?

Expected:

- TLS
    
- mTLS
    
- Certificates
    

---

### 53. Design authentication and authorization for 500 microservices.

---

### 54. How would you manage secrets?

---

### 55. How do you rotate credentials without downtime?

---

# Failure Scenarios

### 56. Payment Service is healthy but responds after 10 seconds.

What happens to the platform?

---

### 57. One service starts producing corrupted events.

How do you contain the blast radius?

---

### 58. Network latency between regions increases by 20x.

How does the architecture behave?

---

### 59. Database replication falls behind by 1 hour.

What failures might users see?

---

### 60. A Kafka cluster becomes unavailable during Black Friday.

Walk through incident response.

---

# Staff/Principal-Level Questions

### 61. When are microservices the wrong architectural choice?

---

### 62. How would you identify a distributed monolith?

Symptoms:

- Shared database
    
- Synchronous chains
    
- Coordinated deployments
    

---

### 63. Your company has 500 microservices.

How would you reduce operational complexity?

---

### 64. How would you measure microservice architecture success?

Metrics:

- Deployment frequency
    
- MTTR
    
- Lead time
    
- Availability
    

---

### 65. If you were redesigning microservices from scratch today, what would you do differently?

This question reveals architectural maturity.

---

# FAANG/Staff-Level Deep Dive Question

One of the toughest:

### 66. Design a global order-processing platform.

Requirements:

```text
100 million orders/day
50 countries
Multi-region
99.99% availability
No double charging
Event-driven
Real-time inventory
```

Discuss:

- Service boundaries
    
- Event design
    
- Consistency model
    
- Failure handling
    
- Scaling strategy
    
- Observability
    
- Disaster recovery
    
- Cost optimization
    

A strong answer to this one touches almost every major microservices concept: domain design, messaging, distributed transactions, resiliency, scalability, and operations. This is the kind of question that separates senior engineers from staff/principal engineers.