"""Tenant-boundary enforcement decorator."""

from domain_security.decorators.tenant_scoped.tenant_scoped_client import (
    TenantScoped,
    tenant_scoped,
)

__all__ = ["TenantScoped", "tenant_scoped"]
