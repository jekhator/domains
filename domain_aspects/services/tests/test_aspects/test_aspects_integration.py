"""Integration tests for aspect composition with real dependencies.

Tests all six aspects with REAL packages from [all] extra. Verifies aspects compose
correctly on function and class targets, catching the bug that existed in 0.1.0
(WrapErrors.build() passing catch incorrectly).
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from domain_aspects import aspects
from domain_aspects.services.aspects import aspects_objects as objs


class TestRealDepsIntegration:
    """Integration tests using real decorator packages."""

    def test_wrap_errors_real_sig_fixed(self) -> None:
        """WrapErrors now calls wrap_errors with correct keyword-only catch arg."""
        from domain_errors import DomainError

        class TestError(DomainError):
            domain = "test"
            code = "error"
            http_status = 500

        @aspects(objs.WrapErrors(as_=TestError, catch=(ValueError,)))
        @dataclass(frozen=True, slots=True)
        class Service:
            def process(self) -> None:
                raise ValueError("inner")

        service = Service()
        with pytest.raises(TestError) as exc_info:
            service.process()
        assert isinstance(exc_info.value.__cause__, ValueError)

    def test_logged_real_sig(self) -> None:
        """Logged calls logged(event) correctly via lazy import."""
        from mixin_logging import LoggingMixin

        @aspects(objs.Logged(event="test.event"))
        @dataclass(frozen=True, slots=True)
        class Service(LoggingMixin):
            def process(self) -> str:
                return "ok"

        service = Service()
        result = service.process()
        assert result == "ok"

    def test_throttled_real_sig(self) -> None:
        """Throttled calls throttled(scope, rate, tiers) correctly."""

        @aspects(objs.Throttled(scope="api", rate="100/hour"))
        @dataclass(frozen=True, slots=True)
        class Service:
            def process(self) -> str:
                return "throttled"

        service = Service()
        result = service.process()
        assert result == "throttled"

    def test_compose_multiple_aspects_no_conflict(self) -> None:
        """Multiple aspects (WrapErrors, Logged, Throttled) compose without conflict."""
        from mixin_logging import LoggingMixin

        from domain_errors import DomainError

        class TestError(DomainError):
            domain = "test"
            code = "error"
            http_status = 500

        @aspects(
            frozenset(
                {
                    objs.Logged(event="multi.test"),
                    objs.Throttled(scope="multi", rate="50/hour"),
                    objs.WrapErrors(as_=TestError),
                }
            )
        )
        @dataclass(frozen=True, slots=True)
        class Service(LoggingMixin):
            def process(self) -> str:
                return "composed"

        service = Service()
        result = service.process()
        assert result == "composed"

    def test_wrap_errors_error_chain_preserved(self) -> None:
        """Composed WrapErrors preserves error chain with __cause__."""
        from domain_errors import DomainError

        class TestError(DomainError):
            domain = "test"
            code = "error"
            http_status = 500

        @aspects(objs.WrapErrors(as_=TestError))
        @dataclass(frozen=True, slots=True)
        class Service:
            def fail(self) -> None:
                raise RuntimeError("root cause")

        service = Service()
        with pytest.raises(TestError) as exc_info:
            service.fail()

        assert exc_info.value.__cause__ is not None
        assert isinstance(exc_info.value.__cause__, RuntimeError)
        assert "root cause" in str(exc_info.value.__cause__)

    def test_requires_real_sig(self) -> None:
        """Requires calls requires(permission) correctly."""
        from domain_security.errors.security_errors import AuthzError

        @aspects(objs.Requires(permission="admin"))
        @dataclass(frozen=True, slots=True)
        class Service:
            def admin_only(self) -> str:
                return "admin_access"

        service = Service()
        with pytest.raises(AuthzError):
            service.admin_only()

    def test_tenant_scoped_real_sig(self) -> None:
        """TenantScoped calls tenant_scoped(param_name) correctly."""
        from domain_security.errors.security_errors import TenancyError

        @aspects(objs.TenantScoped(param_name="tenant_id"))
        @dataclass(frozen=True, slots=True)
        class Service:
            def tenant_method(self, tenant_id: str) -> str:
                return f"tenant:{tenant_id}"

        service = Service()
        with pytest.raises(TenancyError):
            service.tenant_method(tenant_id="test")

    def test_sensitive_real_sig_repr_masking(self) -> None:
        """Sensitive applies mixin-sensitivity repr masking to class."""
        from dataclasses import field

        from mixin_sensitivity import Sensitivity

        @aspects(objs.Sensitive())
        @dataclass(frozen=True, slots=True)
        class Credentials:
            username: str
            password: str = field(metadata={"sensitivity": Sensitivity.SECRET})

        creds = Credentials(username="alice", password="secret123")
        creds_repr = repr(creds)
        assert "secret123" not in creds_repr
        assert "alice" in creds_repr
