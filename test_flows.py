#!/usr/bin/env python3
"""Test script to capture real flow-trace outputs for all five packages."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timezone

# ============================================================================
# domain_errors: DomainError + @wrap_errors
# ============================================================================

print("=" * 80)
print("FLOW-TRACE 1: domain_errors (@wrap_errors)")
print("=" * 80)

from domain_errors import DomainError, wrap_errors
from domain_errors.services.chain.chain_client import ErrorChain


class ValidationError(DomainError):
    """Example domain error."""
    code: str = "validation_failed"
    domain: str = "validation"
    http_status: int = 422
    default_message: str = "Validation failed."


@wrap_errors(as_=ValidationError)
def parse_integer(text: str) -> int:
    """Sync example: ValueError ──▶ ValidationError."""
    return int(text)


try:
    result = parse_integer("not_a_number")
except ValidationError as e:
    print(f"CAUGHT ValidationError: {e.__class__.__name__}")
    print(f"  message: {e.message}")
    print(f"  domain: {e.domain}")
    print(f"  http_status: {e.http_status}")
    print(f"  retryable: {e.retryable}")
    history = ErrorChain.history(e)
    print(f"  chain links: {len(history)}")
    for i, link in enumerate(history):
        print(f"    [{i}] {link.type_name} (domain={link.domain}, via={link.via})")


# ============================================================================
# domain_security: @requires + SecurityContext
# ============================================================================

print("\n" + "=" * 80)
print("FLOW-TRACE 2: domain_security (@requires)")
print("=" * 80)

from domain_security.context.security_context.security_context_client import SecurityContextManager
from domain_security.context.security_context.security_context_objects import Principal, SecurityContext
from domain_security.decorators.requires import requires
from domain_security.errors.security_errors import AuthzError


@requires("admin:read")
def fetch_user(user_id: str) -> dict:
    """Permission-protected method."""
    return {"id": user_id, "name": "Alice"}


# Case 1: Permission check fails (no principal)
print("\nCASE 1: No principal (anonymous)")
try:
    result = fetch_user("123")
except AuthzError as e:
    print(f"CAUGHT AuthzError: {e.__class__.__name__}")
    print(f"  message: {e.message}")
    print(f"  permission: {e.context.get('permission')}")

# Case 2: Permission check passes
print("\nCASE 2: With principal + scope")
principal = Principal(id="user-1", scopes=frozenset(["admin:read", "admin:write"]))
ctx = SecurityContext(principal=principal, tenant_id="tenant-1")
with SecurityContextManager().bind(principal=principal, tenant_id="tenant-1"):
    result = fetch_user("123")
    print(f"SUCCESS: {result}")


# ============================================================================
# domain_api_limiter: @throttled (declaration only, no runtime check)
# ============================================================================

print("\n" + "=" * 80)
print("FLOW-TRACE 3: domain_api_limiter (@throttled)")
print("=" * 80)

from domain_api_limiter.decorators.throttled import throttled
from domain_api_limiter.services.policy.policy_client import PolicyRegistry


@throttled(scope="api:documents", rate="100/hour")
def list_documents() -> list[dict]:
    """Throttled method."""
    return [{"id": "1", "name": "doc.pdf"}]


# Introspect the policy
policy = PolicyRegistry().policy_of(list_documents)
if policy:
    print(f"POLICY ATTACHED: {policy.scope}")
    print(f"  rate: {policy.rate.requests}/{policy.rate.period.value}")
    print(f"  period_seconds: {policy.rate.period_seconds}")
    print(f"  has_tiers: {policy.has_tiers}")
    print(f"  rate.as_rate(): {policy.rate.as_rate()}")

result = list_documents()
print(f"RESULT: {result}")


# ============================================================================
# domain_monitoring: @monitored + metric emission
# ============================================================================

print("\n" + "=" * 80)
print("FLOW-TRACE 4: domain_monitoring (@monitored)")
print("=" * 80)

from domain_monitoring.decorators.monitored.monitored_client import monitored
from domain_monitoring.services.metrics.metrics_client import CollectingSink
from domain_monitoring.services.registry.registry_client import MonitorRegistry


sink = CollectingSink()
MonitorRegistry.set_default_sink(sink)


@monitored("user.fetch")
def fetch_user_monitored(user_id: str) -> dict:
    """Monitored method (success)."""
    return {"id": user_id, "name": "Alice"}


@monitored("user.delete")
def delete_user_monitored(user_id: str) -> None:
    """Monitored method (failure)."""
    raise ValueError(f"Cannot delete {user_id}")


# Success case
print("\nCASE 1: Success metric")
result = fetch_user_monitored("user-1")
events = sink.events
if events:
    e = events[-1]
    print(f"EMITTED MetricEvent: {e.event}")
    print(f"  outcome: {e.outcome}")
    print(f"  duration_ms: {e.duration_ms:.1f}")
    print(f"  occurred_at: {e.occurred_at}")

# Failure case
print("\nCASE 2: Failure metric")
sink.clear()
try:
    delete_user_monitored("user-2")
except ValueError:
    pass
events = sink.events
if events:
    e = events[-1]
    print(f"EMITTED MetricEvent: {e.event}")
    print(f"  outcome: {e.outcome}")
    print(f"  is_failure: {e.is_failure}")
    print(f"  duration_ms: {e.duration_ms:.1f}")


# ============================================================================
# domain_aspects: aspect composition
# ============================================================================

print("\n" + "=" * 80)
print("FLOW-TRACE 5: domain_aspects (composition)")
print("=" * 80)

from domain_aspects.services.aspects.aspects_client import aspects
from domain_aspects.services.aspects.aspects_objects import (
    AspectKind,
    WrapErrors,
    Requires,
    Monitored,
)


sink2 = CollectingSink()


@aspects(
    WrapErrors(as_=ValidationError),
    Requires(permission="data:export"),
    Monitored(event="export.run", sink=sink2),
)
def export_data(tenant_id: str) -> str:
    """Aspect-composed method."""
    # Pretend to export
    if not tenant_id:
        raise ValueError("tenant_id required")
    return "export_completed"


print("\nCOMPOSED aspects on export_data:")
print("  OUTER -> INNER: LOGGED -> REQUIRES -> TENANT_SCOPED -> THROTTLED -> MONITORED -> SENSITIVE -> WRAP_ERRORS")

# Try calling without permission
print("\nCASE 1: No permission (anonymous)")
try:
    result = export_data("tenant-1")
except AuthzError as e:
    print(f"CAUGHT AuthzError (REQUIRES layer): {e.__class__.__name__}")

# Try calling with permission
print("\nCASE 2: With permission + monitor")
principal2 = Principal(id="admin-1", scopes=frozenset(["data:export"]))
MonitorRegistry.set_default_sink(sink2)
sink2.clear()

with SecurityContextManager().bind(principal=principal2, tenant_id="tenant-1"):
    result = export_data("tenant-1")
    print(f"SUCCESS: {result}")
    events = sink2.events
    if events:
        e = events[-1]
        print(f"MONITORED (MONITORED layer): {e.event} (outcome={e.outcome})")


print("\n" + "=" * 80)
print("ALL FLOWS COMPLETE")
print("=" * 80)
