"""Tests for lazy-import behavior and missing optional dependencies."""

from __future__ import annotations

import pytest

import domain_aspects
from domain_aspects.services.aspects import aspects_objects as objs


class TestPublicAPI:
    """Test public API exports."""

    def test_monitored_in_public_api(self) -> None:
        """Monitored is exported from domain_aspects root."""
        assert hasattr(domain_aspects, "Monitored")
        assert "Monitored" in domain_aspects.__all__
        assert domain_aspects.Monitored is objs.Monitored


class TestLazyImports:
    """Test lazy-import behavior and missing optional dependencies."""

    def test_logged_build_missing_mixin_logging(self, monkeypatch) -> None:
        """Logged.build() raises clear error when mixin-logging missing."""
        entry = objs.Logged(event="test")

        def mock_import(*args, **kwargs):
            raise ModuleNotFoundError("No module named 'mixin_logging'")

        monkeypatch.setattr("builtins.__import__", mock_import)
        with pytest.raises(ImportError, match="mixin-logging not installed"):
            entry.build()

    def test_requires_build_missing_domain_security(self, monkeypatch) -> None:
        """Requires.build() raises clear error when domain-security missing."""
        entry = objs.Requires(permission="read")

        def mock_import(*args, **kwargs):
            raise ModuleNotFoundError("No module named 'domain_security'")

        monkeypatch.setattr("builtins.__import__", mock_import)
        with pytest.raises(ImportError, match="domain-security not installed"):
            entry.build()

    def test_tenant_scoped_build_missing_domain_security(self, monkeypatch) -> None:
        """TenantScoped.build() raises clear error when domain-security missing."""
        entry = objs.TenantScoped(param_name="tenant_id")

        def mock_import(*args, **kwargs):
            raise ModuleNotFoundError("No module named 'domain_security'")

        monkeypatch.setattr("builtins.__import__", mock_import)
        with pytest.raises(ImportError, match="domain-security not installed"):
            entry.build()

    def test_throttled_build_missing_domain_api_limiter(self, monkeypatch) -> None:
        """Throttled.build() raises clear error when domain-api-limiter missing."""
        entry = objs.Throttled(scope="api", rate="100/hour")

        def mock_import(*args, **kwargs):
            raise ModuleNotFoundError("No module named 'domain_api_limiter'")

        monkeypatch.setattr("builtins.__import__", mock_import)
        with pytest.raises(ImportError, match="domain-api-limiter not installed"):
            entry.build()

    def test_wrap_errors_build_missing_domain_errors(self, monkeypatch) -> None:
        """WrapErrors.build() raises clear error when domain-errors missing."""
        entry = objs.WrapErrors(as_=ValueError)

        def mock_import(*args, **kwargs):
            if "domain_errors" in str(args):
                raise ModuleNotFoundError("No module named 'domain_errors'")
            return __import__(*args, **kwargs)

        monkeypatch.setattr("builtins.__import__", mock_import)
        with pytest.raises(ImportError, match="domain-errors not installed"):
            entry.build()

    def test_monitored_build_missing_domain_monitoring(self, monkeypatch) -> None:
        """Monitored.build() raises clear error when domain-monitoring missing."""
        entry = objs.Monitored(event="metric")

        def mock_import(*args, **kwargs):
            raise ModuleNotFoundError("No module named 'domain_monitoring'")

        monkeypatch.setattr("builtins.__import__", mock_import)
        with pytest.raises(ImportError, match="domain-monitoring not installed"):
            entry.build()

    def test_sensitive_build_missing_mixin_sensitivity(self, monkeypatch) -> None:
        """Sensitive.build() raises clear error when mixin-sensitivity missing."""
        entry = objs.Sensitive()

        def mock_import(*args, **kwargs):
            raise ModuleNotFoundError("No module named 'mixin_sensitivity'")

        monkeypatch.setattr("builtins.__import__", mock_import)
        with pytest.raises(ImportError, match="mixin-sensitivity not installed"):
            entry.build()

    def test_entries_validatable_without_optional_deps(self) -> None:
        """Entry objects fully validatable without importing optional deps."""
        entries: list[objs.AspectEntry] = [
            objs.Logged(event="test"),
            objs.Monitored(event="metric"),
            objs.Requires(permission="read"),
            objs.Sensitive(),
            objs.TenantScoped(param_name="tenant_id"),
            objs.Throttled(scope="api", rate="100/hour"),
            objs.WrapErrors(as_=ValueError),
        ]
        for entry in entries:
            assert entry.kind is not None
            assert hash(entry) is not None
