"""Fixtures for authorization tests."""

from __future__ import annotations

import pytest

from domain_security.context.security_context.security_context_objects import (
    Principal,
    SecurityContext,
)
from domain_security.services.authz.authz_objects import Permission


@pytest.fixture
def permission() -> Permission:  # fixture
    """Create a permission."""
    return Permission(value="read")


@pytest.fixture
def write_permission() -> Permission:  # fixture
    """Create a write permission."""
    return Permission(value="write")


@pytest.fixture
def delete_permission() -> Permission:  # fixture
    """Create a delete permission."""
    return Permission(value="delete")


@pytest.fixture
def principal_with_read_scope() -> Principal:  # fixture
    """Create a principal with read scope."""
    return Principal(id="user:reader", roles=frozenset(), scopes=frozenset(["read"]))


@pytest.fixture
def principal_with_multiple_scopes() -> Principal:  # fixture
    """Create a principal with multiple scopes."""
    return Principal(
        id="user:admin",
        roles=frozenset(["admin"]),
        scopes=frozenset(["read", "write", "delete"]),
    )


@pytest.fixture
def context_with_principal(  # fixture
    principal_with_read_scope: Principal,
) -> SecurityContext:
    """Create a security context with a principal."""
    return SecurityContext(principal=principal_with_read_scope, tenant_id="tenant:test")
