"""Rate-limit declaration toolkit for Python services."""

from domain_api_limiter.config._version import __version__
from domain_api_limiter.decorators.throttled.throttled_client import throttled
from domain_api_limiter.errors.api_limiter_errors import (
    RateLimitExceeded,
    ThrottleDeclarationError,
    ThrottleError,
)
from domain_api_limiter.services.policy.policy_client import PolicyRegistry
from domain_api_limiter.services.policy.policy_objects import (
    Period,
    RateLimit,
    ThrottlePolicy,
    TierRate,
)

__all__ = [
    "Period",
    "PolicyRegistry",
    "RateLimit",
    "RateLimitExceeded",
    "ThrottleDeclarationError",
    "ThrottleError",
    "ThrottlePolicy",
    "TierRate",
    "__version__",
    "throttled",
]
