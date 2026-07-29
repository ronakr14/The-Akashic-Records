# AI Summary:
ronak
# Plugins That Can Be Added

> See also: [[cli2api System Architecture#7. Plugin Engine]] | [[cli2api Feature Roadmap and Enhancements#9. Plugin System]] | [[06 Constraints#3. Plugins are Hooks, Not Injection]]

## Plugin Architecture Overview

Plugins are **well-defined hooks with strict contracts** — not arbitrary middleware injection. They follow a "middleware with contracts" model: each plugin implements a fixed interface, and the execution engine calls them in a predictable order.

## Plugin Interface (Strict Contract)

```python
# plugins/base.py
class Plugin:
    def before_request(self, request, config, kwargs):
        """Called before function execution. Can modify/validate kwargs."""
        return kwargs

    def after_response(self, request, response, config):
        """Called after function execution. Can transform response."""
        return response

    def on_error(self, request, error, config):
        """Called on exception. Can suppress, log, or transform errors."""
        raise error

    def on_startup(self, app):
        """Called when app starts. Use for resource initialization."""
        pass
```

## Execution Order

```
Request arrives
  -> before_request (forward order as listed)
  -> Function executes
  -> after_response (reverse order / stack unwind)
  -> Response returned

If exception:
  -> on_error (forward order)
  -> Error re-raised or suppressed
```

## Plugin Registry

```python
# plugins/registry.py
PLUGINS = {}

def register_plugin(name: str, plugin):
    PLUGINS[name] = plugin

def get_plugin(name: str):
    if name not in PLUGINS:
        raise Exception(f"Plugin {name} not found")
    return PLUGINS[name]
```

## YAML Configuration

```yaml
# Global plugins (applied to all routes)
plugins:
  - logging
  - rate_limit

# Per-route plugins (override globals)
routes:
  - name: process_data
    plugins: [auth, rate_limit, idempotency]
```

---

## Built-in Plugins

### 1. Logging Plugin

Logs every request with method, URL, and parameters.

```python
# plugins/logging.py
class LoggingPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        logger.info(f"{request.method} {request.url} | {kwargs}")
        return kwargs
```

### 2. Rate Limit Plugin

Redis-backed atomic rate limiting per IP + route.

```python
# plugins/rate_limit.py
class RateLimitPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        limit = config.get("rate_limit", 10)
        key = f"rate:{request.client.host}:{config['name']}"
        count = redis_client.incr(key)
        if count == 1:
            redis_client.expire(key, 60)
        if count > limit:
            raise Exception("Rate limit exceeded")
        return kwargs
```

### 3. Idempotency Plugin

Prevents duplicate execution via client-provided key.

```python
# plugins/idempotency.py
class IdempotencyPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        key = request.headers.get("Idempotency-Key")
        if not key:
            return kwargs
        existing = get_key(key)
        if existing:
            if existing["status"] == "completed":
                raise CachedResponse(existing["response"])
            raise Exception("Still processing")
        set_processing(key)
        request.state.idem_key = key
        return kwargs

    def after_response(self, request, response, config):
        key = getattr(request.state, "idem_key", None)
        if key:
            set_completed(key, response)
        return response
```

### 4. Auth Plugin

API key or JWT validation.

```python
# plugins/auth.py
class AuthPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        api_key = request.headers.get("x-api-key")
        if api_key not in get_valid_keys():
            raise HTTPException(401, "Invalid API Key")
        return kwargs
```

---

## Plugins That Can Be Added

### 5. Caching Plugin

Cache function responses by request parameters.

```python
# plugins/caching.py
class CachingPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        cache_key = f"cache:{config['name']}:{hash(kwargs)}"
        cached = redis_client.get(cache_key)
        if cached:
            raise CachedResponse(json.loads(cached))
        request.state.cache_key = cache_key
        return kwargs

    def after_response(self, request, response, config):
        cache_key = getattr(request.state, "cache_key", None)
        if cache_key:
            redis_client.setex(cache_key, 300, json.dumps(response))
        return response
```

### 6. Metrics Plugin

Prometheus metrics per endpoint.

```python
# plugins/metrics.py
class MetricsPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        REQUEST_COUNT.labels(route=config["name"]).inc()
        request.state.start_time = time.time()
        return kwargs

    def after_response(self, request, response, config):
        duration = time.time() - request.state.start_time
        REQUEST_LATENCY.labels(route=config["name"]).observe(duration)
        return response
```

### 7. Tracing Plugin

OpenTelemetry distributed tracing.

```python
# plugins/tracing.py
class TracingPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        span = tracer.start_span(f"cli2api.{config['name']}")
        request.state.span = span
        return kwargs

    def after_response(self, request, response, config):
        request.state.span.finish()
        return response
```

### 8. Validation Plugin

Additional business validation beyond type hints.

```python
# plugins/validation.py
class ValidationPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        # Custom validation rules from config
        rules = config.get("validation_rules", {})
        for field, rule in rules.items():
            if field in kwargs:
                if not rule(kwargs[field]):
                    raise ValidationError(f"{field} failed validation")
        return kwargs
```

### 9. Notification Plugin

Send notifications on task completion.

```python
# plugins/notification.py
class NotificationPlugin(Plugin):
    def after_response(self, request, response, config):
        if config.get("notify_on_complete"):
            send_notification(config["name"], response)
        return response
```

### 10. Audit Plugin

Audit trail for sensitive operations.

```python
# plugins/audit.py
class AuditPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        audit_log.info({
            "action": config["name"],
            "client": request.client.host,
            "params": kwargs,
            "timestamp": datetime.utcnow().isoformat()
        })
        return kwargs
```

### 11. Circuit Breaker Plugin

Prevent cascade failures.

```python
# plugins/circuit_breaker.py
class CircuitBreakerPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        key = f"circuit:{config['name']}"
        state = redis_client.get(key)
        if state == "open":
            raise ServiceUnavailable("Circuit breaker is open")
        return kwargs

    def on_error(self, request, error, config):
        key = f"circuit:{config['name']}"
        failures = redis_client.incr(f"{key}:failures")
        if failures > 5:
            redis_client.setex(key, 60, "open")
        raise error
```

### 12. Retry Plugin

Automatic retry with backoff for transient failures.

```python
# plugins/retry.py
class RetryPlugin(Plugin):
    def on_error(self, request, error, config):
        retries = getattr(request.state, "retries", 0)
        if retries < 3 and is_transient(error):
            request.state.retries = retries + 1
            time.sleep(2 ** retries)  # exponential backoff
            raise RetryException()
        raise error
```

### 13. Feature Flag Plugin

Enable/disable routes dynamically.

```python
# plugins/feature_flag.py
class FeatureFlagPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        flag = config.get("feature_flag")
        if flag and not is_feature_enabled(flag):
            raise HTTPException(404, "Feature not available")
        return kwargs
```

### 14. Request Transform Plugin

Normalize/transform incoming requests.

```python
# plugins/request_transform.py
class RequestTransformPlugin(Plugin):
    def before_request(self, request, config, kwargs):
        # e.g., convert string dates to datetime objects
        transforms = config.get("transforms", {})
        for field, transform in transforms.items():
            if field in kwargs:
                kwargs[field] = transform(kwargs[field])
        return kwargs
```

### 15. Response Transform Plugin

Format responses (e.g., camelCase for JS consumers).

```python
# plugins/response_transform.py
class ResponseTransformPlugin(Plugin):
    def after_response(self, request, response, config):
        if config.get("camel_case"):
            response = to_camel_case(response)
        return response
```

---

## Plugin Config Support

Plugins can accept their own configuration:

```yaml
plugins:
  - name: rate_limit
    config:
      requests: 10
      window: 60
  - name: auth
    config:
      roles: ["admin"]
      jwt_secret: "${JWT_SECRET}"
```

## Plugin Dependency System

Declare ordering constraints:

```yaml
auth:
  requires: [logging]  # logging always runs before auth
rate_limit:
  requires: []         # no dependencies
```

## Plugin Discovery (Entry Points)

Allow pip-installable third-party plugins:

```toml
[project.entry-points."cli2api.plugins"]
my_plugin = "my_plugin_package:register"
```

```python
# my_plugin_package.py
def register():
    from plugins.registry import register_plugin
    register_plugin("my_plugin", MyPlugin())
```

## Plugin Pitfalls to Avoid

> Also see: [[06 Constraints#3. Plugins are Hooks, Not Injection]] | [[06 Constraints#9. Plugin Hell]]

1. **Plugin order matters** — `[idempotency, rate_limit]` != `[rate_limit, idempotency]`
2. **Hidden side effects** — plugins that mutate `kwargs` unpredictably create debugging nightmares
3. **Too many plugins** — if every feature becomes a plugin, you've reinvented middleware hell
4. **Plugins with state** — keep plugins stateless; use Redis for shared state
5. **Breaking the contract** — plugins must respect the interface, not bypass it



```yaml
title: cli2api Plugin Architecture and Plugin Catalog

folder: Projects/cli2api/Architecture

categorical:
  domain:
    value: architecture
    reason: Defines the extensibility architecture, plugin lifecycle, contracts, and built-in plugin ecosystem of the framework.

  subdomain: plugin-architecture

  note_type:
    value: architecture
    reason: Documents the plugin subsystem, execution model, configuration, and extension mechanisms rather than implementation tasks.

  source_type:
    value: self
    reason: Self-authored architectural specification.

  status:
    value: curated
    reason: Well-defined architectural reference that should evolve only as the plugin framework changes.

  level:
    value: advanced
    reason: Covers framework extensibility, lifecycle hooks, dependency management, distributed infrastructure, and production design patterns.

ratings:
  confidence:
    score: 5
    reason: Self-authored design document with no external factual claims.

  completeness:
    score: 5
    reason: Covers plugin contracts, lifecycle, execution order, registry, configuration, built-in plugins, extension model, dependency resolution, and implementation pitfalls.

  complexity:
    score: 5
    reason: Describes a complete extensibility framework involving lifecycle hooks, plugin orchestration, configuration, and infrastructure integration.

  importance:
    score: 5
    reason: The plugin system is a core architectural pillar that enables extensibility across the entire platform.

  career_relevance:
    score: 5
    reason: Demonstrates framework engineering, software architecture, inversion of control, extensibility, and platform design skills.

  freshness:
    score: 5
    reason: Includes modern framework capabilities such as Redis-backed plugins, OpenTelemetry, feature flags, plugin discovery, dependency ordering, and structured configuration.

  reusability:
    score: 5
    reason: The architectural patterns can be applied to many SDKs, internal platforms, and extensible frameworks.

  review_priority:
    score: 3
    reason: Stable architectural reference that should be reviewed when new plugins or lifecycle hooks are introduced.

  connectedness:
    score: 5
    reason: Serves as a hub linking the execution engine, YAML configuration, plugin implementations, Redis, observability, and framework constraints.

  actionability:
    score: 4
    reason: Provides concrete plugin interfaces and implementation guidance while leaving plugin development to separate notes.

  quality_score:
    score: 99
    reason: Comprehensive specification covering architecture, lifecycle, extensibility, configuration, operational concerns, and best practices for a production-grade plugin system.

custom:
  tags:
    - cli2api
    - plugins
    - architecture
    - extensibility
    - redis

ai_summary: >
  Defines the plugin architecture for cli2api, including the lifecycle contract, execution order, registry, configuration model, and extensibility mechanisms. Plugins operate through constrained lifecycle hooks (before_request, after_response, on_error, on_startup) rather than arbitrary middleware injection. The document specifies YAML-based plugin configuration, dependency ordering, plugin discovery through Python entry points, configuration validation, and a catalog of built-in plugins including logging, authentication, rate limiting, idempotency, caching, metrics, tracing, notifications, circuit breakers, retries, feature flags, and request/response transformations. It also documents architectural pitfalls and best practices for maintaining a predictable plugin ecosystem. :contentReference[oaicite:0]{index=0} :contentReference[oaicite:1]{index=1}
```

### Classification rationale

This note is another **Architecture** note rather than a project or technology note because it defines the **extensibility subsystem** of `cli2api`.

Your documentation hierarchy is becoming very clean:

```text
Projects/
└── cli2api/
    ├── 00 README.md
    ├── 01 Goal.md
    ├── 02 Architecture.md
    ├── 03 Steps to Implement.md
    ├── 04 Enhancements.md
    ├── 05 Plugin Architecture.md   ← this note
    ├── 06 Constraints.md
    ├── 07 Typer Integration.md
    ├── 08 Argparse Integration.md
    ├── 09 Rich Integration.md
    ├── 10 Examples.md
    └── ADR/
```

One suggestion: rename the note from **"Plugins That Can Be Added"** to **"Plugin Architecture and Catalog"** (or **"Plugin System"**). The current title suggests it's just a list of plugins, but most of the document actually specifies the architecture, lifecycle, configuration, dependency system, discovery mechanism, and design rules. The plugin catalog is only one part of the content.