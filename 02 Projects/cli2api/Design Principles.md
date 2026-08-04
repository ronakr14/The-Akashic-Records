---
domain: architecture
subdomain: architecture-principles
source_type: architecture
note_type: self
status: curated
level: advanced
tags:
  - cli2api
  - architecture
  - design-principles
  - constraints
  - clean-architecture
---
# AI Summary
Defines the architectural constraints and engineering principles that govern cli2api. The document establishes rules such as keeping business logic framework-agnostic, treating YAML as a declarative control plane, enforcing plugins as constrained lifecycle hooks, deriving all execution surfaces from function signatures, validating configuration at startup, and preferring strong defaults over excessive configuration. It also documents common anti-patterns—including infrastructure leakage, god decorators, plugin overuse, tight framework coupling, and silent configuration errors—and concludes with practical guidance on production trade-offs and long-term framework evolution. 

---
# Design Constraints (Must Follow)

### 1. Functions Must Stay Pure

Business logic functions must never import or reference:
- FastAPI (no Request, HTTPException, Depends)
- Celery (no @celery_app.task)
- Redis (no redis_client)
- Any framework-specific decorator or middleware

The function is the contract. If it needs infra, it goes in plugins or the execution layer.

**Why**: When functions are coupled to FastAPI or Celery, you can't reuse them in other contexts. The whole point is a single function that works everywhere.

### 2. YAML is a Control Plane, Not an Execution Engine

YAML should only contain:
- Route config (path, method)
- Rate limits
- Auth requirements
- Async vs sync flag
- Plugin selection
- Tagging / grouping

YAML should NEVER contain:
- Business logic
- Conditional flows
- Data transformations
- Code expressions or lambdas

**Why**: YAML that contains logic becomes untestable, unversionable, and unreadable. Keep it declarative.

### 3. Plugins are Hooks, Not Injection

Plugins must implement the 4-hook contract. They must not:
- Replace the function entirely
- Bypass the execution pipeline
- Access each other's internal state
- Modify the function signature

**Why**: Arbitrary middleware injection turns the system into an unpredictable maze. Constrained hooks keep debugging sane.

### 4. Keep Plugin Set Minimal

If every feature becomes a plugin, you've reinvented middleware hell.

Rule of thumb: if something can be a simple if-statement in the endpoint factory, don't make it a plugin.

**Why**: More plugins = more complexity = more failure modes. Only plugin-ify cross-cutting concerns that apply to multiple routes.

### 5. Order of Plugins Matters

```yaml
plugins: [idempotency, rate_limit]  # Check idempotency first, then rate limit
plugins: [rate_limit, idempotency]  # Rate limit first, then idempotency
```

These are NOT equivalent. Document or enforce order.

**Why**: Plugin execution is sequential. Idempotency check before rate limit means repeated requests skip rate limiting. Reverse means every repeated request counts against the limit.

### 6. Function Signature is the Single Source of Truth

CLI args, API params, and validation all derive from the function signature. Do NOT:
- Define separate CLI argument schemas
- Create duplicate Pydantic models when type hints suffice
- Manually map function params to different names per surface

**Why**: Duplication breaks the "one contract" principle. Change the function, and all surfaces update automatically.

### 7. Fail Fast on Config Errors

YAML misconfigurations must crash at startup, not silently break at runtime:
- YAML references unregistered function -> crash
- Invalid plugin name -> crash
- Missing required fields -> crash

**Why**: Silent misconfigurations (wrong route, missing plugin) cause mysterious 404s or 500s in production. Startup validation catches them immediately.

### 8. Keep Defaults Strong, Overrides Minimal

Sensible defaults should cover 80% of use cases. YAML should only override what's different:

```yaml
defaults:
  auth: true
  rate_limit: 10
  async_task: false
  idempotency: true

routes:
  - name: health
    auth: false   # Only override what differs from defaults
```

**Why**: If every knob is in YAML, nobody knows what's happening. Strong defaults reduce cognitive load.

---

## Anti-Patterns (Must Avoid)

### 1. Mixing Business Logic with Infrastructure

```python
# BAD
@expose
def process_data(x: int):
    redis_client.set(f"last_result_{x}", x * 2)  # infra leak
    return x * 2

# GOOD
@expose
def process_data(x: int):
    return x * 2
# Caching handled by a plugin if needed
```

### 2. God Decorator

```python
# BAD — decorator does everything
@expose(path="/api", method="POST", auth=True, rate_limit=10,
        cache=True, notify=True, retry=3, ...)
def process_data(x: int):
    ...

# GOOD — decorator registers, YAML configures
@expose
def process_data(x: int):
    ...
# config.yaml owns: path, method, auth, rate_limit, etc.
```

### 3. In-Memory State in Production

```python
# BAD — in-memory rate limiting
RATE_LIMIT_STORE = {}  # Doesn't work across processes/servers

# GOOD — Redis-backed
redis_client.incr(key)  # Atomic, shared across all instances
```

### 4. Function Signatures That Drift from API Contracts

```python
# BAD — changing function breaks clients silently
def process_data(x: int, y: int):  # Was (x: int)
    ...

# GOOD — version your API contracts, use deprecation
# Or use Pydantic models for stable contracts
```

### 5. Tight Coupling to FastAPI

```python
# BAD — function imports FastAPI
from fastapi import Request

@expose
def process_data(request: Request, x: int):  # API-specific
    ...

# GOOD — function is framework-agnostic
@expose
def process_data(x: int):
    ...
# Request context accessed by framework layer, not the function
```

### 6. Over-Configurability

```yaml
# BAD — every tiny detail in YAML
routes:
  - name: process_data
    path: /process
    method: POST
    auth: true
    rate_limit: 10
    rate_limit_window: 60
    rate_limit_strategy: sliding_window
    retry_count: 3
    retry_backoff: exponential
    cache_ttl: 300
    cache_strategy: lru
    log_level: INFO
    log_format: json
    ...  # 20 more lines per route
```

### 7. No Idempotency for Async Jobs

```python
# BAD — async job can execute multiple times
@celery_app.task
def process_payment(amount):
    charge_card(amount)  # Retried = double charge

# GOOD — idempotent with key
@celery_app.task
def process_payment(amount, idempotency_key):
    if already_processed(idempotency_key):
        return get_cached_result(idempotency_key)
    result = charge_card(amount)
    mark_completed(idempotency_key, result)
    return result
```

### 8. Silent Misconfigurations

```python
# BAD — typo silently ignored
routes:
  - name: procss_data  # typo, no error
    path: /process

# GOOD — startup validation
# Raises: "Function procss_data not registered. Did you mean process_data?"
```

### 9. Plugin Hell

```yaml
# BAD — 15 plugins per route, no clear purpose
plugins: [auth, rate_limit, cache, metrics, tracing, audit,
          feature_flag, circuit_breaker, retry, notification,
          validation, transform, logging, throttle, ...]
```

### 10. Not Versioning API Contracts

```python
# BAD — changing function signature breaks clients
def add(a: int, b: int) -> dict:  # Returns {"result": N}
    return {"result": a + b}

# Later changed to:
def add(a: int, b: int) -> int:  # Now returns plain int
    return a + b  # All clients break
```

---

## Hard Truths
1. **This pattern is great for internal tools**, not ideal for public APIs without versioning and error contracts.
2. **In-memory rate limiting is fake safety** — use Redis in production.
3. **API keys in code are a liability** — move to env vars, DB, or secrets manager.
4. **Function signatures are not stable API contracts** — if you refactor blindly, you will break clients.
5. **You're ~2 steps away from building your own framework** — decide early if this is a personal power tool or a team platform. Each requires different investment.
6. **Plugins are where these setups go off the rails** — if plugins can do "anything anywhere," you lose control of execution flow.
7. **Async jobs without idempotency are duplication machines** — retries will cause duplicate side effects.
8. **YAML that contains logic becomes unmaintainable** — keep it declarative control only.