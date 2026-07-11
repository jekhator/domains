# domain-suite

Consolidated domain packages for Python services: typed errors, security context, API rate limiting, event monitoring, and cross-cutting aspects.

[![PyPI](https://img.shields.io/pypi/v/domain-suite.svg)](https://pypi.org/project/domain-suite/)
[![CI](https://github.com/jekhator/domain-suite/workflows/CI/badge.svg)](https://github.com/jekhator/domain-suite/actions)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python versions](https://img.shields.io/pypi/pyversions/domain-suite.svg)](https://pypi.org/project/domain-suite/)

## Overview

**domain-suite** brings together five complementary domain packages into a single distribution:

- **domain-errors**: Typed domain error hierarchy with wrapping and chaining
- **domain-security**: Security context management and authorization checks
- **domain-api-limiter**: Request rate limiting and quota enforcement
- **domain-monitoring**: Event monitoring and telemetry
- **domain-aspects**: Composable decorators for logging, auth, throttling, error wrapping, and sensitivity masking

Each package maintains its namespace and API; the consolidation is organizational (single distribution, unified testing).

## Installation

```bash
# Base install
uv add domain-suite

# With all optional extras (logging + sensitivity)
uv add "domain-suite[all]"

# Or select extras
uv add "domain-suite[logging]"    # for mixin-logging support
uv add "domain-suite[sensitivity]" # for mixin-sensitivity support
```

or with pip:

```bash
pip install domain-suite
pip install "domain-suite[all]"
```

Requires Python 3.11+.

## Packages

### domain-errors

Typed domain error hierarchy with wrapping and chaining for Python services.

**Public API:**
`DomainError`, `ErrorChain`, `WrapErrorsClient`, `wrap_errors`, `ChainLink`, `ChainVia`, `DomainClassifier`, `DomainCrossing`.

**Example:**

```python
from domain_errors import DomainError, wrap_errors

class DatabaseError(DomainError):
    domain = "database"
    code = "db_connection_failed"
    http_status = 503
    retryable = True

@wrap_errors(as_=DatabaseError)
def fetch_user(user_id: str):
    # ... implementation
    pass
```

See `docs/domain_errors/` for full documentation.

### domain-security

Security context management and authorization checks.

**Public API:**
`SecurityContext`, `SecurityContextManager`, `Principal`, `requires`, `tenant_scoped`, `Authorizer`, `Permission`, `PolicyDecision`, `SecretRef`, `SecretValue`, security error classes.

**Example:**

```python
from domain_security import SecurityContext, SecurityContextManager, requires

# Set security context
ctx = SecurityContext(user_id="usr_123", tenant_id="org_abc", claims={"role": "admin"})
SecurityContextManager.set(ctx)

# Enforce authorization via decorator
@requires(permission="admin.read")
def admin_only_function():
    return "Admin access granted"
```

See `docs/domain_security/` for full documentation.

### domain-api-limiter

Request rate limiting and quota enforcement.

**Public API:**
`throttled`, `PolicyRegistry`, `RateLimit`, `ThrottlePolicy`, `TierRate`, `Period`, `RateLimitExceeded`, throttle error classes.

**Example:**

```python
from domain_api_limiter import throttled

@throttled(scope="api.documents", rate="100/hour")
def create_document(title: str):
    return {"id": "doc_123", "title": title}
```

See `docs/domain_api_limiter/` for full documentation.

### domain-monitoring

Event monitoring and telemetry.

**Public API:**
`monitored`, `MonitorRegistry`, `MetricSink`, `MetricEvent`, `Outcome`, `CollectingSink`, `NullSink`, monitoring error classes.

**Example:**

```python
from domain_monitoring import monitored, MonitorRegistry

@monitored(event="document.processed")
def process_document(doc_id: str):
    return {"status": "success"}
```

See `docs/domain_monitoring/` for full documentation.

### domain-aspects

Composable decorators for logging, auth, throttling, error wrapping, and sensitivity masking.

**Public API:**
`aspects`, `Logged`, `Requires`, `Throttled`, `TenantScoped`, `WrapErrors`, `Sensitive`, `AspectEntry`, `AspectKind`, aspect error classes.

**Example:**

```python
from domain_aspects import aspects, Logged, Requires, Throttled

@aspects(
    Logged(event="document.create"),
    Requires(permission="documents.write"),
    Throttled(scope="api.documents", rate="100/hour"),
)
def create_document(title: str, content: str) -> dict:
    return {"id": "doc_123", "title": title}
```

See `docs/domain_aspects/` for full documentation.

## Consolidated From

This distribution consolidates five independent domain packages (originally `domain-errors`, `domain-security`, `domain-api-limiter`, `domain-monitoring`, and `domain-aspects`) into a single unified distribution to simplify dependency management and testing.

Each package retains its original public API and namespace. Internal dependencies between packages within the suite are resolved locally (no external package re-imports required).

## Optional Extras

- **`[logging]`**: Integrates with `mixin-logging>=0.6.0` for structured event logging adapters.
- **`[sensitivity]`**: Integrates with `mixin-sensitivity>=0.4.0` for automatic PII/PHI field masking.
- **`[all]`**: Includes both `mixin-logging` and `mixin-sensitivity`.

Future versions may introduce new extras or migrate integrations (e.g., `mixin-suite` packages if they consolidate similarly).

## Development

Install development dependencies:

```bash
uv sync --all-extras
```

Run tests:

```bash
uv run pytest
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
