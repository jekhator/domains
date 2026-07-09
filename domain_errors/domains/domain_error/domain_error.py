"""DomainError: base class for per-project typed exception hierarchies."""

from __future__ import annotations

from domain_errors.domains.constants import domain_error as const


class DomainError(Exception):
    """Base for per-project typed exception hierarchies."""

    code: str = const.DEFAULT_CODE
    domain: str = const.DEFAULT_DOMAIN

    http_status: int = const.DEFAULT_HTTP_STATUS
    default_message: str = const.DEFAULT_MESSAGE
    retryable: bool = False

    def __init__(self, message: str | None = None, **context: object) -> None:
        """Store the message and logger context, then initialize Exception."""
        self.message = message or self.default_message
        self.context = context
        super().__init__(self.message)
