"""Tenant-boundary enforcement against the ambient security context."""

from __future__ import annotations

from domain_security.context.security_context.security_context_objects import (
    SecurityContext,
)
from domain_security.errors.security_errors import TenancyError
from domain_security.services.constants import tenancy as const


class TenancyGuard:
    """Verify that an operation stays inside the context's tenant boundary."""

    def check(self, ctx: SecurityContext, tenant_id: str) -> None:
        """Raise TenancyError unless the context is bound to the given tenant."""
        if ctx.tenant_id is None:
            raise TenancyError(
                message=const.ERR_TENANCY_NO_TENANT_BOUND,
                tenant_id=tenant_id,
            )
        if ctx.tenant_id != tenant_id:
            raise TenancyError(
                message=const.ERR_TENANCY_BOUNDARY_VIOLATION,
                tenant_id=tenant_id,
                context_tenant_id=ctx.tenant_id,
            )
