"""Aspect entry validation constants. Imported as const."""

from __future__ import annotations

from typing import Final

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
