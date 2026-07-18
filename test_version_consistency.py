"""Test that all domain roots report consistent versions."""

from __future__ import annotations


class TestVersionConsistency:
    """Test version consistency across all domain roots."""

    def test_all_roots_same_version(self) -> None:
        """All 6 domain roots should report identical __version__."""
        import domain_api_limiter
        import domain_aspects
        import domain_errors
        import domain_monitoring
        import domain_rag
        import domain_security

        versions = {
            "domain_api_limiter": domain_api_limiter.__version__,
            "domain_aspects": domain_aspects.__version__,
            "domain_errors": domain_errors.__version__,
            "domain_monitoring": domain_monitoring.__version__,
            "domain_rag": domain_rag.__version__,
            "domain_security": domain_security.__version__,
        }

        unique_versions = set(versions.values())
        assert (
            len(unique_versions) == 1
        ), f"Version mismatch: {versions}"
        assert versions["domain_errors"] == "0.3.0"
