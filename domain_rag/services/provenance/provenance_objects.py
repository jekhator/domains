"""Retrieval provenance event DTO. Frozen, hashable, immutable."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Final


class ProvenanceOutcome(StrEnum):
    """Retrieval provenance outcome enumeration."""

    SUCCESS: Final = "success"
    FAILURE: Final = "failure"


@dataclass(frozen=True, slots=True)
class RetrievalProvenance:
    """Immutable retrieval provenance event with audit trail."""

    query: str
    chunk_ids: tuple[str, ...]
    source_document_ids: tuple[str, ...]
    principal_id: str
    session_id: str
    outcome: ProvenanceOutcome
    duration_ms: float
    occurred_at: str

    def __post_init__(self) -> None:
        """Validate retrieval provenance invariants."""
        if not self.query:
            raise ValueError("query must be non-empty")
        if not self.principal_id:
            raise ValueError("principal_id must be non-empty")
        if not self.session_id:
            raise ValueError("session_id must be non-empty")
        if self.duration_ms < 0:
            raise ValueError("duration_ms must be non-negative")
        if not self.occurred_at:
            raise ValueError("occurred_at must be non-empty")

    def __hash__(self) -> int:
        """Hash event by all fields for set membership."""
        return hash(
            (
                self.query,
                self.chunk_ids,
                self.source_document_ids,
                self.principal_id,
                self.session_id,
                self.outcome,
                self.duration_ms,
                self.occurred_at,
            )
        )

    @classmethod
    def for_success(
        cls,
        query: str,
        chunk_ids: tuple[str, ...],
        source_document_ids: tuple[str, ...],
        principal_id: str,
        session_id: str,
        duration_ms: float,
        occurred_at: str,
    ) -> "RetrievalProvenance":
        """Create a success retrieval provenance event."""
        return cls(
            query=query,
            chunk_ids=chunk_ids,
            source_document_ids=source_document_ids,
            principal_id=principal_id,
            session_id=session_id,
            outcome=ProvenanceOutcome.SUCCESS,
            duration_ms=duration_ms,
            occurred_at=occurred_at,
        )

    @classmethod
    def for_failure(
        cls,
        query: str,
        principal_id: str,
        session_id: str,
        duration_ms: float,
        occurred_at: str,
    ) -> "RetrievalProvenance":
        """Create a failure retrieval provenance event."""
        return cls(
            query=query,
            chunk_ids=(),
            source_document_ids=(),
            principal_id=principal_id,
            session_id=session_id,
            outcome=ProvenanceOutcome.FAILURE,
            duration_ms=duration_ms,
            occurred_at=occurred_at,
        )

    @property
    def is_failure(self) -> bool:
        """Check if provenance represents a failure."""
        return self.outcome == ProvenanceOutcome.FAILURE
