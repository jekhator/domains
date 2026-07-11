"""Aspect composition and ordering constants.

Imported as const.
"""

from __future__ import annotations

from typing import Final

__all__ = [
    "ASPECT_ORDER",
    "ERR_ASPECTS_DUPLICATE_KIND",
    "ERR_ASPECTS_UNKNOWN_ENTRY_TYPE",
    "ERR_ASPECTS_EMPTY_DECLARATION",
    "ERR_ASPECTS_DECLARATION_FAILED",
]


"""Aspect application order (innermost-to-outermost: WRAP_ERRORS innermost, LOGGED outermost)."""

ASPECT_ORDER: Final = (
    "LOGGED",
    "REQUIRES",
    "TENANT_SCOPED",
    "THROTTLED",
    "MONITORED",
    "SENSITIVE",
    "WRAP_ERRORS",
)


"""Aspect declaration validation error messages."""

ERR_ASPECTS_DUPLICATE_KIND: Final = "Duplicate aspect kind in declaration: {kind}."

ERR_ASPECTS_UNKNOWN_ENTRY_TYPE: Final = "Unknown aspect entry type: {entry_type}."

ERR_ASPECTS_EMPTY_DECLARATION: Final = "Aspect declaration is empty."

ERR_ASPECTS_DECLARATION_FAILED: Final = "Aspect declaration failed."
