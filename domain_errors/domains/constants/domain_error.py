"""Domain error defaults. Imported as const."""

from __future__ import annotations

from typing import Final

__all__ = [
    "DEFAULT_CODE",
    "DEFAULT_DOMAIN",
    "DEFAULT_HTTP_STATUS",
    "DEFAULT_MESSAGE",
]


"""Base-class contract defaults; consumer subclasses override these per error type."""

DEFAULT_CODE: Final = "domain_error"
DEFAULT_DOMAIN: Final = "application"
DEFAULT_HTTP_STATUS: Final = 500
DEFAULT_MESSAGE: Final = "An unspecified domain error occurred."
