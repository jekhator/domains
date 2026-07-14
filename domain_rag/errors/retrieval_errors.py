"""Retrieval domain errors. Imported as const.ERR_*."""

from domain_errors import DomainError
from domain_rag.errors.constants import retrieval as const


class RetrievalError(DomainError):
    """Retrieval operation failed."""

    domain = "retrieval"
    http_status = 500
    retryable = False
    default_message = const.ERR_RETRIEVAL_FAILED


class RetrievalDeclarationError(DomainError):
    """Invalid decorator target or declaration."""

    domain = "retrieval"
    http_status = 500
    retryable = False
    default_message = const.ERR_RETRIEVAL_INVALID_TARGET
