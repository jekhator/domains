"""Aspect entry value objects for decorator composition."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from domain_monitoring.services.metrics.metrics_client import MetricSink


class AspectKind(StrEnum):
    """Aspect classification kinds."""

    LOGGED = "LOGGED"
    REQUIRES = "REQUIRES"
    TENANT_SCOPED = "TENANT_SCOPED"
    THROTTLED = "THROTTLED"
    MONITORED = "MONITORED"
    WRAP_ERRORS = "WRAP_ERRORS"
    SENSITIVE = "SENSITIVE"


@dataclass(frozen=True, slots=True)
class Logged:
    """Lazy-import logging mixin, emit event on entry and exit."""

    event: str

    def __post_init__(self) -> None:
        if not self.event or not isinstance(self.event, str):
            raise ValueError("Logged.event must be a non-empty string.")

    @property
    def kind(self) -> AspectKind:
        return AspectKind.LOGGED

    def build(self) -> Callable:
        """Lazily import and apply logged decorator."""
        try:
            from mixin_logging import logged
        except ImportError as e:
            raise ImportError(
                "mixin-logging not installed; add [logging] extra."
            ) from e
        return logged(self.event)


@dataclass(frozen=True, slots=True)
class Requires:
    """Permission check via domain-security."""

    permission: str

    def __post_init__(self) -> None:
        if not self.permission or not isinstance(self.permission, str):
            raise ValueError("Requires.permission must be a non-empty string.")

    @property
    def kind(self) -> AspectKind:
        return AspectKind.REQUIRES

    def build(self) -> Callable:
        """Lazily import and apply requires decorator."""
        try:
            from domain_security.decorators.requires import requires
        except ImportError as e:
            raise ImportError(
                "domain-security not installed; add [security] extra."
            ) from e
        return requires(self.permission)


@dataclass(frozen=True, slots=True)
class TenantScoped:
    """Tenant isolation enforcement via domain-security."""

    param_name: str = "tenant_id"

    def __post_init__(self) -> None:
        if not self.param_name or not isinstance(self.param_name, str):
            raise ValueError("TenantScoped.param_name must be a non-empty string.")

    @property
    def kind(self) -> AspectKind:
        return AspectKind.TENANT_SCOPED

    def build(self) -> Callable:
        """Lazily import and apply tenant_scoped decorator."""
        try:
            from domain_security.decorators.tenant_scoped import tenant_scoped
        except ImportError as e:
            raise ImportError(
                "domain-security not installed; add [security] extra."
            ) from e
        return tenant_scoped(self.param_name)


@dataclass(frozen=True, slots=True)
class Throttled:
    """Rate limiting via domain-api-limiter."""

    scope: str
    rate: str
    tiers: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not self.scope or not isinstance(self.scope, str):
            raise ValueError("Throttled.scope must be a non-empty string.")
        if not self.rate or not isinstance(self.rate, str):
            raise ValueError("Throttled.rate must be a non-empty string.")
        if not isinstance(self.tiers, tuple):
            raise ValueError("Throttled.tiers must be a tuple of pairs.")

    @property
    def kind(self) -> AspectKind:
        return AspectKind.THROTTLED

    def build(self) -> Callable:
        """Lazily import and apply throttled decorator."""
        try:
            from domain_api_limiter.decorators.throttled import throttled
        except ImportError as e:
            raise ImportError(
                "domain-api-limiter not installed; add [throttle] extra."
            ) from e
        tiers_dict = dict(self.tiers) if self.tiers else None
        return throttled(self.scope, self.rate, tiers=tiers_dict)


@dataclass(frozen=True, slots=True)
class WrapErrors:
    """Exception wrapping and translation via domain-errors."""

    as_: type
    catch: tuple[type[BaseException], ...] = (Exception,)

    def __post_init__(self) -> None:
        if not isinstance(self.as_, type):
            raise ValueError("WrapErrors.as_ must be an exception class.")
        if not self.catch or not isinstance(self.catch, tuple):
            raise ValueError(
                "WrapErrors.catch must be a non-empty tuple of exception types."
            )

    @property
    def kind(self) -> AspectKind:
        return AspectKind.WRAP_ERRORS

    def build(self) -> Callable:
        """Import and apply wrap_errors decorator."""
        try:
            from domain_errors import wrap_errors
        except ImportError as e:
            raise ImportError(
                "domain-errors not installed; it is a hard dependency."
            ) from e
        return wrap_errors(as_=self.as_, catch=self.catch)  # type: ignore[arg-type]


@dataclass(frozen=True, slots=True)
class Monitored:
    """Metric emission via domain-monitoring."""

    event: str
    sink: Optional[MetricSink] = None

    def __post_init__(self) -> None:
        if not self.event or not isinstance(self.event, str):
            raise ValueError("Monitored.event must be a non-empty string.")

    @property
    def kind(self) -> AspectKind:
        return AspectKind.MONITORED

    def build(self) -> Callable:
        """Lazily import and apply monitored decorator."""
        try:
            from domain_monitoring.decorators.monitored.monitored_client import (
                monitored,
            )
        except ImportError as e:
            raise ImportError(
                "domain-monitoring not installed; it is a hard dependency."
            ) from e
        return monitored(self.event, sink=self.sink)


@dataclass(frozen=True, slots=True)
class Sensitive:
    """Sensitive field masking via mixin-sensitivity."""

    def __post_init__(self) -> None:
        pass

    @property
    def kind(self) -> AspectKind:
        return AspectKind.SENSITIVE

    def build(self) -> Callable:
        """Lazily import and apply sensitive decorator."""
        try:
            from mixin_sensitivity import sensitive
        except ImportError as e:
            raise ImportError(
                "mixin-sensitivity not installed; add [sensitivity] extra."
            ) from e
        return sensitive


AspectEntry = (
    Logged | Requires | TenantScoped | Throttled | Monitored | WrapErrors | Sensitive
)
"""Union type alias for all aspect entry types."""
