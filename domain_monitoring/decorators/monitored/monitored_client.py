"""Monitored decorator for automatic metric emission."""

import asyncio
import functools
import inspect
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any, Optional, TypeVar, cast

from domain_monitoring.errors.constants import monitoring as const
from domain_monitoring.errors.monitoring_errors import MonitoringDeclarationError
from domain_monitoring.services.metrics.metrics_client import MetricSink
from domain_monitoring.services.metrics.metrics_objects import MetricEvent
from domain_monitoring.services.registry.registry_client import MonitorRegistry

Target = TypeVar("Target")


def monitored(
    event: str, sink: Optional[MetricSink] = None
) -> Callable[[Target], Target]:
    """Apply metric tracking to callables and classes."""

    def decorator(target: Target) -> Target:
        """Apply monitoring to target."""
        if inspect.isclass(target):
            return cast(Target, _monitor_class(target, event, sink))
        elif callable(target):
            return cast(Target, _monitor_callable(target, event, sink))
        else:
            raise MonitoringDeclarationError(const.ERR_MONITORING_INVALID_TARGET)

    return decorator


def _monitor_callable(
    fn: Callable[..., Any], event: str, sink: Optional[MetricSink]
) -> Callable[..., Any]:
    """Wrap a callable with monitoring."""
    if asyncio.iscoroutinefunction(fn):
        return _wrap_async(fn, event, sink)
    else:
        return _wrap_sync(fn, event, sink)


def _wrap_sync(
    fn: Callable[..., Any], event: str, sink: Optional[MetricSink]
) -> Callable[..., Any]:
    """Wrap synchronous callable."""

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Execute with metric tracking."""
        start_time = datetime.now(timezone.utc)
        actual_sink = sink or MonitorRegistry.get_default_sink()

        try:
            result = fn(*args, **kwargs)
            end_time = datetime.now(timezone.utc)
            duration_ms = (end_time - start_time).total_seconds() * 1000
            metric_event = MetricEvent.for_success(
                event=event,
                duration_ms=duration_ms,
                occurred_at=end_time.isoformat(),
            )
            actual_sink.emit(metric_event)
            return result
        except Exception:
            end_time = datetime.now(timezone.utc)
            duration_ms = (end_time - start_time).total_seconds() * 1000
            metric_event = MetricEvent.for_failure(
                event=event,
                duration_ms=duration_ms,
                occurred_at=end_time.isoformat(),
            )
            actual_sink.emit(metric_event)
            raise

    return wrapper


def _wrap_async(
    fn: Callable[..., Any], event: str, sink: Optional[MetricSink]
) -> Callable[..., Any]:
    """Wrap asynchronous callable."""

    @functools.wraps(fn)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        """Execute async with metric tracking."""
        start_time = datetime.now(timezone.utc)
        actual_sink = sink or MonitorRegistry.get_default_sink()

        try:
            result = await fn(*args, **kwargs)
            end_time = datetime.now(timezone.utc)
            duration_ms = (end_time - start_time).total_seconds() * 1000
            metric_event = MetricEvent.for_success(
                event=event,
                duration_ms=duration_ms,
                occurred_at=end_time.isoformat(),
            )
            actual_sink.emit(metric_event)
            return result
        except Exception:
            end_time = datetime.now(timezone.utc)
            duration_ms = (end_time - start_time).total_seconds() * 1000
            metric_event = MetricEvent.for_failure(
                event=event,
                duration_ms=duration_ms,
                occurred_at=end_time.isoformat(),
            )
            actual_sink.emit(metric_event)
            raise

    return async_wrapper


def _monitor_class(cls: type, event: str, sink: Optional[MetricSink]) -> type:
    """Fan out monitoring to public methods on a class."""
    public_methods = _get_public_methods(cls)

    if not public_methods:
        raise MonitoringDeclarationError(const.ERR_MONITORING_EMPTY_CLASS)

    for method_name in public_methods:
        original_method = getattr(cls, method_name)
        derived_event = f"{event}.{method_name}"
        monitored_method = _monitor_callable(original_method, derived_event, sink)
        setattr(cls, method_name, monitored_method)

    return cls


def _get_public_methods(cls: type) -> list[str]:
    """Get public method names from class, excluding inherited and special methods."""
    public = []

    for name, value in inspect.getmembers(cls):
        if name.startswith("_"):
            continue
        if inspect.ismethod(value) or inspect.isfunction(value):
            if not hasattr(cls, "__bases__") or name not in dir(cls.__bases__[0]):
                public.append(name)
        elif isinstance(value, classmethod):  # pragma: no cover
            public.append(name)
        elif isinstance(value, staticmethod):  # pragma: no cover
            public.append(name)

    return public
