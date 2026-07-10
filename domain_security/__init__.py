"""Cross-cutting security concerns: authorization, tenancy, secrets, context management."""

from domain_security.config._version import __version__
from domain_security.context.security_context.security_context_client import (
    SecurityContextManager,
)
from domain_security.context.security_context.security_context_objects import (
    Principal,
    SecurityContext,
)
from domain_security.decorators.requires.requires_client import requires
from domain_security.decorators.tenant_scoped.tenant_scoped_client import tenant_scoped
from domain_security.errors.security_errors import (
    AuthzError,
    SecretError,
    SecurityDeclarationError,
    SecurityError,
    TenancyError,
)
from domain_security.services.authz.authz_client import Authorizer
from domain_security.services.authz.authz_objects import Permission, PolicyDecision
from domain_security.services.secrets.secrets_client import SecretRef
from domain_security.services.secrets.secrets_objects import SecretValue

__all__ = [
    "Authorizer",
    "AuthzError",
    "Permission",
    "PolicyDecision",
    "Principal",
    "SecretError",
    "SecretRef",
    "SecretValue",
    "SecurityContext",
    "SecurityContextManager",
    "SecurityDeclarationError",
    "SecurityError",
    "TenancyError",
    "__version__",
    "requires",
    "tenant_scoped",
]
