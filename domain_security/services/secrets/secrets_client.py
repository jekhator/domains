"""Secret references resolved at call time through a pluggable backend."""

from __future__ import annotations

from domain_errors import wrap_errors
from domain_security.errors.security_errors import SecretError
from domain_security.services.constants import secrets as const
from domain_security.services.secrets import secrets_objects as objs


class SecretRef:
    """Named reference to a secret, resolved lazily against a backend."""

    def __init__(self, name: str) -> None:
        """Store the secret name for later resolution."""
        self.name = name

    @wrap_errors(SecretError, capture=False)
    def resolve(self, backend: objs.SecretsBackend | None = None) -> objs.SecretValue:
        """Fetch the named secret from the backend and wrap it in a SecretValue."""
        if backend is None:
            raise SecretError(
                message=const.ERR_SECRETS_NO_BACKEND,
                secret_name=self.name,
            )
        return objs.SecretValue(backend.fetch(self.name))
