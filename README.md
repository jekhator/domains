# domains

Consolidated domain packages for Python services: typed errors, security context, API rate limiting, event monitoring, and cross-cutting aspects.

## Overview

**domains** brings together five complementary packages into a single distribution:

- **domain-errors**: Typed domain error hierarchy with wrapping and chaining
- **domain-security**: Security context management and authorization checks
- **domain-api-limiter**: Request rate limiting and quota enforcement
- **domain-monitoring**: Event monitoring and telemetry
- **domain-aspects**: Composable decorators for logging, auth, throttling, error wrapping, and sensitivity masking

Each package maintains its namespace and API; the consolidation is organizational (single distribution, unified testing).

## Installation

```bash
uv add domains
```

or with pip:

```bash
pip install domains
```

Requires Python 3.11+.

## Packages

### domain-errors

Typed domain error hierarchy with wrapping and chaining for Python services.

```python
from domain_errors import DomainError, ErrorChain

class DatabaseError(DomainError):
    domain = "database"
    code = "db_error"
    http_status = 503
    retryable = True

try:
    user = db.query("SELECT * FROM users WHERE id = $1", user_id)
except Exception as e:
    raise ErrorChain.wrap(
        e,
        as_=DatabaseError,
        message=f"Failed to fetch user {user_id}",
        user_id=user_id
    ) from e
```

See `docs/errors/` for full documentation.

### domain-security

Security context management and authorization checks.

```python
from domain_security import SecurityContext, Requires

# Set security context
ctx = SecurityContext(user_id="usr_123", tenant_id="org_abc", claims={"role": "admin"})
SecurityContextManager.set(ctx)

# Enforce authorization via decorator
@Requires(permission="admin.read")
def admin_only_function():
    return "Admin access granted"
```

See `docs/security/` for full documentation.

### domain-api-limiter

Request rate limiting and quota enforcement.

```python
from domain_api_limiter import ApiLimiter, RateLimitExceeded

limiter = ApiLimiter()

try:
    limiter.check_limit("api.documents", rate="100/hour")
except RateLimitExceeded:
    return {"error": "Rate limit exceeded"}, 429
```

See `docs/api_limiter/` for full documentation.

### domain-monitoring

Event monitoring and telemetry.

```python
from domain_monitoring import MonitorRegistry, EventSink

sink = EventSink()
registry = MonitorRegistry()
registry.set_default_sink(sink)

registry.log_event("document.processed", {"doc_id": "doc_123", "status": "success"})
```

See `docs/monitoring/` for full documentation.

### domain-aspects

Composable decorators for logging, auth, throttling, error wrapping, and sensitivity masking.

```python
from domain_aspects import aspects

@aspects(
    aspects.Logged(event="document.create"),
    aspects.Requires(permission="documents.write"),
    aspects.Throttled(scope="api.documents", rate="100/hour"),
    aspects.Sensitive(),
)
def create_document(title: str, content: str) -> dict:
    return {"id": "doc_123", "title": title}
```

See `docs/aspects/` for full documentation.

## Development

Install development dependencies:

```bash
uv sync
```

Run tests:

```bash
pytest
```

Run linting and type checking:

```bash
ruff check .
ruff format --check .
mypy
```

## License

Apache License 2.0. See LICENSE for details.

## Contributing

See CONTRIBUTING.md for guidelines.
