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
    "ERR_ASPECT_LOGGED_EVENT_EMPTY",
    "ERR_ASPECT_REQUIRES_PERMISSION_EMPTY",
    "ERR_ASPECT_TENANT_SCOPED_PARAM_EMPTY",
    "ERR_ASPECT_THROTTLED_SCOPE_EMPTY",
    "ERR_ASPECT_THROTTLED_RATE_EMPTY",
    "ERR_ASPECT_THROTTLED_TIERS_NOT_TUPLE",
    "ERR_ASPECT_WRAP_ERRORS_AS_NOT_CLASS",
    "ERR_ASPECT_WRAP_ERRORS_CATCH_INVALID",
    "ERR_ASPECT_MONITORED_EVENT_EMPTY",
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


"""Aspect entry validation error messages."""

ERR_ASPECT_LOGGED_EVENT_EMPTY: Final = "Logged.event must be a non-empty string."

ERR_ASPECT_REQUIRES_PERMISSION_EMPTY: Final = (
    "Requires.permission must be a non-empty string."
)

ERR_ASPECT_TENANT_SCOPED_PARAM_EMPTY: Final = (
    "TenantScoped.param_name must be a non-empty string."
)

ERR_ASPECT_THROTTLED_SCOPE_EMPTY: Final = "Throttled.scope must be a non-empty string."

ERR_ASPECT_THROTTLED_RATE_EMPTY: Final = "Throttled.rate must be a non-empty string."

ERR_ASPECT_THROTTLED_TIERS_NOT_TUPLE: Final = (
    "Throttled.tiers must be a tuple of pairs."
)

ERR_ASPECT_WRAP_ERRORS_AS_NOT_CLASS: Final = (
    "WrapErrors.as_ must be an exception class."
)

ERR_ASPECT_WRAP_ERRORS_CATCH_INVALID: Final = (
    "WrapErrors.catch must be a non-empty tuple of exception types."
)

ERR_ASPECT_MONITORED_EVENT_EMPTY: Final = "Monitored.event must be a non-empty string."
