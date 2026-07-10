"""Fixtures for tenancy tests."""

from __future__ import annotations

import pytest

from domain_security.context.security_context.security_context_objects import (
    Principal,
    SecurityContext,
)


@pytest.fixture
def principal() -> Principal:  # fixture
    """Create a principal."""
    return Principal(id="user:test", roles=frozenset(), scopes=frozenset())


@pytest.fixture
def context_with_tenant(principal: Principal) -> SecurityContext:  # fixture
    """Create a context with a tenant."""
    return SecurityContext(principal=principal, tenant_id="tenant:acme")


@pytest.fixture
def context_without_tenant(principal: Principal) -> SecurityContext:  # fixture
    """Create a context without a tenant."""
    return SecurityContext(principal=principal, tenant_id=None)
