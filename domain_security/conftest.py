"""Root pytest configuration for domain_security package."""

from __future__ import annotations

import pytest

from domain_security.context.security_context.security_context_client import (
    SecurityContextManager,
)


@pytest.fixture(autouse=True)
def reset_security_context() -> None:
    """Reset security context to clean state before each test."""
    SecurityContextManager._context.set(None)
