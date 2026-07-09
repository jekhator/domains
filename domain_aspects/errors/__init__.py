"""Error hierarchy for aspect composition."""

from __future__ import annotations

from domain_aspects.errors.aspects_errors import (
    AspectDeclarationError,
    AspectsError,
)

__all__ = ["AspectsError", "AspectDeclarationError"]
