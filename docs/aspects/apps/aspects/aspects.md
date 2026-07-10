# Aspects Service

Composable aspect decorators for stacking cross-cutting concerns.

## Overview

The Aspects service enables declarative composition of six cross-cutting aspects: logging, authorization, tenancy, throttling, error wrapping, and sensitive field masking.

Key design:

- **Immutable entries**: All aspect entries are frozen dataclasses with hashable fields for frozenset membership.
- **Lazy imports**: Optional dependencies (mixin-logging, domain-security, domain-api-limiter, mixin-sensitivity) are imported only when an entry's `build()` method is called, so validation works without them installed.
- **Canonical ordering**: Aspects apply in ASPECT_ORDER regardless of declaration order (LOGGED outermost, WRAP_ERRORS innermost).
- **Validation at decoration time**: Duplicate kinds, unknown entry types, and empty declarations raise AspectDeclarationError.

## Entry Types

### Logged

```python
Logged(event: str)
```

Emit entry and exit events via mixin-logging.

### Requires

```python
Requires(permission: str)
```

Check permissions against a security context via domain-security.

### TenantScoped

```python
TenantScoped(param_name: str = "tenant_id")
```

Enforce tenant isolation via domain-security.

### Throttled

```python
Throttled(scope: str, rate: str, tiers: tuple[tuple[str, str], ...] = ())
```

Apply rate limiting via domain-api-limiter. Tiers are optional per-tier rate overrides.

### WrapErrors

```python
WrapErrors(as_: type, catch: tuple[type[BaseException], ...] = (Exception,))
```

Translate exceptions to a target exception type via domain-errors.

### Sensitive

```python
Sensitive()
```

Mask sensitive fields in repr via mixin-sensitivity.

## Usage

### Single Entry

```python
@aspects(Logged(event="service.method"))
def method(self) -> None:
    pass
```

### Frozenset

```python
@aspects(frozenset({
    Logged(event="service.method"),
    Requires(permission="admin.read"),
    Sensitive(),
}))
def method(self) -> None:
    pass
```

### Mixed

```python
@aspects(
    Logged(event="service.method"),
    frozenset({Requires(permission="admin.read")}),
    Sensitive(),
)
def method(self) -> None:
    pass
```

## Error Handling

Declaration-time validation raises AspectDeclarationError when:

- Duplicate aspect kinds (e.g., two Logged entries).
- Unknown entry type (not one of the six official types).
- Empty declaration (frozenset or argument list with no entries).

## Optional Dependencies

Each aspect has an optional extra for its underlying library:

- `[logging]` — mixin-logging
- `[security]` — domain-security
- `[throttle]` — domain-api-limiter
- `[sensitivity]` — mixin-sensitivity
- `[all]` — all four

Install with:

```bash
pip install domain-aspects[all]
```

## Ordering

Aspects apply in this canonical order (innermost-to-outermost):

1. LOGGED (outermost: emits start/exit events)
2. REQUIRES (permission check)
3. TENANT_SCOPED (tenant boundary enforcement)
4. THROTTLED (rate limiting)
5. SENSITIVE (sensitive field masking)
6. WRAP_ERRORS (innermost: exception translation)

This order is enforced by the Aspects service during composition, regardless of the order you declare entries.
