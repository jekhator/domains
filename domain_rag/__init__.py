"""Domain RAG library: vendor-neutral retrieval provenance tracking."""

from domain_rag.config._version import __version__
from domain_rag.decorators.traced_retrieval.traced_retrieval_client import (
    traced_retrieval,
)
from domain_rag.errors.retrieval_errors import (
    RetrievalDeclarationError,
    RetrievalError,
)
from domain_rag.services.provenance.provenance_client import (
    CollectingProvenanceSink,
    NullProvenanceSink,
    ProvenanceSink,
)
from domain_rag.services.provenance.provenance_objects import (
    ProvenanceOutcome,
    RetrievalProvenance,
)
from domain_rag.services.registry.registry_client import ProvenanceRegistry

__all__ = [
    "__version__",
    "CollectingProvenanceSink",
    "NullProvenanceSink",
    "ProvenanceOutcome",
    "ProvenanceRegistry",
    "ProvenanceSink",
    "RetrievalDeclarationError",
    "RetrievalError",
    "RetrievalProvenance",
    "traced_retrieval",
]
