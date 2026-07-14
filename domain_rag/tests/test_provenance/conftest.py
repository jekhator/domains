"""Fixtures for provenance tests."""

import pytest

from domain_rag.services.provenance.provenance_client import CollectingProvenanceSink


@pytest.fixture
def collecting_sink() -> CollectingProvenanceSink:
    """Provide a collecting provenance sink."""
    return CollectingProvenanceSink()
