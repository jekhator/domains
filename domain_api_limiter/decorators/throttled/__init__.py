"""Rate-limit declaration decorator."""

from domain_api_limiter.decorators.throttled.throttled_client import (
    Throttled,
    throttled,
)

__all__ = ["Throttled", "throttled"]
