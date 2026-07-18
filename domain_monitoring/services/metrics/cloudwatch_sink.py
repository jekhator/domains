"""CloudWatch metric sink for production metric emission."""

from __future__ import annotations

from datetime import datetime
from typing import TypedDict

from domain_monitoring.errors.constants import monitoring as const
from domain_monitoring.services.metrics.metrics_objects import MetricEvent


class _MetricDatapoint(TypedDict, total=False):
    """Metric data point for AWS CloudWatch put_metric_data API."""

    MetricName: str
    Value: float
    Unit: str
    Timestamp: datetime
    Dimensions: list[dict[str, str]]


class CloudWatchMetricSink:
    """Emit MetricEvent to AWS CloudWatch via boto3."""

    def __init__(self, namespace: str = "domain-monitoring") -> None:
        """Initialize CloudWatch sink.

        Args:
            namespace: CloudWatch namespace for metrics.

        Raises:
            ImportError: If boto3 is not installed.
        """
        try:
            import boto3
        except ImportError as e:  # pragma: no cover
            raise ImportError(const.ERR_MONITORING_BOTO3_MISSING) from e

        self.namespace = namespace
        self._cloudwatch = boto3.client("cloudwatch")

    def emit(self, event: MetricEvent) -> None:
        """Emit metric event to CloudWatch.

        Args:
            event: MetricEvent with outcome, duration, and labels.
        """
        metric_point: _MetricDatapoint = {
            "MetricName": event.event,
            "Value": event.duration_ms,
            "Unit": "Milliseconds",
            "Timestamp": datetime.fromisoformat(event.occurred_at),
            "Dimensions": self._build_dimensions(event),
        }
        self._cloudwatch.put_metric_data(
            Namespace=self.namespace,
            MetricData=[metric_point],
        )

    @staticmethod
    def _build_dimensions(event: MetricEvent) -> list[dict[str, str]]:
        """Build CloudWatch dimensions from metric event labels and outcome.

        Args:
            event: MetricEvent with labels and outcome.

        Returns:
            List of dimension dicts for CloudWatch.
        """
        dimensions: list[dict[str, str]] = [
            {"Name": "Outcome", "Value": event.outcome.value}
        ]

        for label_key, label_value in event.labels:
            dimensions.append({"Name": label_key, "Value": label_value})

        return dimensions
