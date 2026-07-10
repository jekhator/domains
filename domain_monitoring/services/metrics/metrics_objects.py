"""Metric event DTO. Frozen, hashable, immutable."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Final


class Outcome(StrEnum):
    """Metric outcome enumeration."""

    SUCCESS: Final = "success"
    FAILURE: Final = "failure"


@dataclass(frozen=True, slots=True)
class MetricEvent:
    """Immutable metric event with outcome tracking."""

    event: str
    outcome: Outcome
    duration_ms: float
    occurred_at: str
    labels: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        """Validate metric event invariants."""
        if not self.event:
            raise ValueError("event must be non-empty")
        if self.duration_ms < 0:
            raise ValueError("duration_ms must be non-negative")
        if not self.occurred_at:
            raise ValueError("occurred_at must be non-empty")

    def __hash__(self) -> int:
        """Hash event by all fields for set membership."""
        return hash(
            (self.event, self.outcome, self.duration_ms, self.occurred_at, self.labels)
        )

    @classmethod
    def for_success(
        cls,
        event: str,
        duration_ms: float,
        occurred_at: str,
        labels: tuple[tuple[str, str], ...] = (),
    ) -> "MetricEvent":
        """Create a success metric event."""
        return cls(
            event=event,
            outcome=Outcome.SUCCESS,
            duration_ms=duration_ms,
            occurred_at=occurred_at,
            labels=labels,
        )

    @classmethod
    def for_failure(
        cls,
        event: str,
        duration_ms: float,
        occurred_at: str,
        labels: tuple[tuple[str, str], ...] = (),
    ) -> "MetricEvent":
        """Create a failure metric event."""
        return cls(
            event=event,
            outcome=Outcome.FAILURE,
            duration_ms=duration_ms,
            occurred_at=occurred_at,
            labels=labels,
        )

    @property
    def is_failure(self) -> bool:
        """Check if metric represents a failure."""
        return self.outcome == Outcome.FAILURE
