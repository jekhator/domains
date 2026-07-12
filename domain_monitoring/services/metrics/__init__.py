"""Metric sink protocol and event collection."""

from domain_monitoring.services.metrics.metrics_client import (
    CollectingSink,
    MetricSink,
    NullSink,
)
from domain_monitoring.services.metrics.metrics_objects import MetricEvent

__all__ = ["CollectingSink", "MetricEvent", "MetricSink", "NullSink"]
