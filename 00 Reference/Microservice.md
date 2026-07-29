# AI Summary
Microservices. A microservice is a small, independent application responsible for one business capability. Microservices organize systems around **business domains** rather than technical layers

```table-of-contents
```

# Microservices

A microservice is a small, independent application responsible for one business capability. Microservices organize systems around **business domains** rather than technical layers.

## Mental Model

| Metaphor | Characteristics |
|---|---|
| **Monolith** | One large factory — simple to manage, hard to scale selectively |
| **Microservices** | Many specialized factories — easy to scale individually, harder to coordinate |
| **Distributed System** | Entire city of factories — networking, communication, failures, and coordination become primary challenges |

Microservices are really an application of distributed systems. The next logical step after understanding microservices is learning consistency, partitioning, replication, consensus, messaging, and fault tolerance.

## Why Microservices

Monoliths work well initially. Problems appear when:

- Codebase becomes huge with hundreds of developers
- Deployments become risky (one bad change takes down everything)
- Scaling requirements differ across modules

Example: Reporting module becomes busy. With a monolith, you scale the entire application. With microservices, you scale only the Reporting Service.

## Core Principles

### Domain-Driven Design ([[DDD]])

Organize around business capabilities, not technical layers:

```
Not this:                This:
  Database Team            Order Team
  UI Team                 Payment Team
  API Team                Customer Team
```

Each team owns everything for that domain — logic, data, deployment, quality.

### Service Independence

Each service must be able to develop, deploy, and scale independently. Order Service v1 can deploy while Payment Service v2 deploys — no coordinated releases.

### Database Ownership

Each microservice owns its own database. No service may directly access another service's tables. This enforces clear ownership and prevents tight coupling.

```
Order Service    → Order DB
Payment Service  → Payment DB
User Service     → User DB
```

Without this separation, you get a distributed monolith — microservices in name only, with all the downsides of both approaches.

## Architecture

```
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

## Service Communication

### Synchronous

Like a phone call — the caller waits for a response. Protocols: HTTP/REST, [[gRPC]].

```
Order Service → Payment Service (waits for response)
```

Use when: the result is needed immediately to proceed.

### Asynchronous

Like sending a message — the caller doesn't wait. Brokers: [[Apache Kafka]], [[RabbitMQ]], [[Apache Pulsar]].

```
Order Service → Message Queue → Payment Service
```

Use when: the caller can continue without immediate confirmation; throughput and decoupling matter more than latency.

### Event-Driven Pattern

A common microservices pattern built on asynchronous communication:

```
Order Created
      |
      +--> Inventory Updated
      +--> Email Sent
      +--> Analytics Updated
```

Services react to events independently. Very scalable, but introduces challenges: event ordering, duplication, replay, and debugging.

## API Gateway

Clients should not call services directly. A gateway handles:

- Routing
- Authentication
- Rate limiting
- Logging

Popular options: [[Kong]], [[NGINX]], [[Spring Cloud Gateway]].

## Service Discovery

Services come and go dynamically (scaling, deployments, failures). A service registry tracks locations:

- Service registers itself on startup
- Other services query the registry to find it

Options: [[Consul]], [[Eureka]], [[etcd]].

## Fault Tolerance

Microservices assume failures. Three core mechanisms:

| Mechanism | When to use |
|---|---|
| **Retry** | Transient failures — try again with backoff |
| **Timeout** | Slow dependency — stop waiting after threshold |
| **Circuit Breaker** | Repeated failures — temporarily stop sending requests to prevent cascading failures |
| **Bulkhead** | Resource isolation — failure in one area doesn't exhaust resources for others |

## Distributed Transactions

The hardest problem in microservices. Consider:

```
Create Order → Charge Card → Update Inventory
```

If inventory fails after payment succeeds, the customer is charged with no inventory reserved.

### [[Saga Pattern]]

Break the transaction into steps with compensating actions:

```
Step 1: Create Order
Step 2: Charge Card
Step 3: Reserve Inventory

If Step 3 fails:
  Compensate: Refund Payment → Cancel Order
```

Two variants: **Choreography** (each service emits events for the next) and **Orchestration** (a coordinator drives the flow).

## Observability

Debugging a monolith: one log file. Debugging microservices: hundreds of services, thousands of requests.

Three pillars:

| Pillar | What it answers | Tools |
|---|---|---|
| **Logs** | What happened? | ELK Stack, Loki |
| **Metrics** | How healthy? | [[Prometheus]], [[Grafana]] |
| **Traces** | Request journey across services | [[Jaeger]], [[OpenTelemetry]] |

Distributed tracing follows a request through every service it touches, enabling root-cause analysis across the entire call chain.

## Deployment

### Containers

Microservices are typically packaged as [[Docker]] containers — lightweight, portable, consistent environments.

### Orchestration

Running hundreds of containers requires orchestration. [[Kubernetes]] handles:

- Scheduling (place containers on nodes)
- Scaling (add/remove instances)
- Self-healing (restart failed containers)
- Networking (service-to-service communication)
- Rolling updates (deploy without downtime)

### Deployment Strategies

| Strategy | Description |
|---|---|
| **Blue-Green** | Two identical environments; switch traffic instantly |
| **Canary** | Route small % of traffic to new version, gradually increase |
| **Rolling** | Replace instances one at a time |
| **Shadow** | Mirror production traffic to new version without affecting users |

## Advantages

- **Faster development** — teams work independently
- **Independent deployments** — no giant coordinated releases
- **Independent scaling** — scale only busy services
- **Technology flexibility** — each service can use the best language/framework for its needs

## Disadvantages

Microservices solve monolith problems by introducing distributed systems problems. You trade code complexity for operational complexity.

New challenges:

- Network failures and retries
- Service discovery
- Data consistency across services
- Distributed transactions
- Monitoring and debugging across services
- Security across service boundaries

## When NOT to Use Microservices

**Start with a monolith** when:

- Team is small (< 10 engineers)
- Product requirements are unclear
- You need fast iteration speed
- You don't have platform engineering or DevOps capability

Companies like Amazon, Netflix, and Uber evolved toward microservices after reaching significant scale — not on day one.

## Technology Ecosystem

| Concern | Tools |
|---|---|
| **API Gateway** | [[Kong]], [[NGINX]], [[Spring Cloud Gateway]] |
| **Service Discovery** | [[Consul]], [[Eureka]], [[etcd]] |
| **Message Brokers** | [[Apache Kafka]], [[RabbitMQ]], [[Apache Pulsar]] |
| **Containers** | [[Docker]] |
| **Orchestration** | [[Kubernetes]] |
| **Metrics** | [[Prometheus]], [[Grafana]] |
| **Tracing** | [[Jaeger]], [[OpenTelemetry]] |
| **Logging** | ELK Stack, Loki |
| **Service Mesh** | [[Istio]], [[Linkerd]] |

## Related

- [[Distributed Systems]]
- [[Domain-Driven Design]]
- [[Saga Pattern]]
- [[API Gateway]]
- [[Kubernetes]]
- [[Docker]]
- [[Apache Kafka]]
- [[Observability]]
- [[CAP Theorem]]
- [[Microservice Anti-Patterns]]
