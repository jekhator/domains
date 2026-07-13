"""Tests for @monitored decorator."""

import asyncio
from dataclasses import dataclass

import pytest

from domain_monitoring.decorators.monitored.monitored_client import monitored
from domain_monitoring.errors.monitoring_errors import MonitoringDeclarationError
from domain_monitoring.services.metrics.metrics_client import CollectingSink
from domain_monitoring.services.metrics.metrics_objects import Outcome
from domain_monitoring.services.registry.registry_client import MonitorRegistry


class TestMonitoredOnCallable:
    """@monitored on functions and methods."""

    def setup_method(self) -> None:
        """Clear registry before each test."""
        MonitorRegistry.clear_default_sink()

    def test_monitored_sync_callable_success(self) -> None:
        """@monitored on sync callable emits SUCCESS event."""
        sink = CollectingSink()

        @monitored("test.operation", sink=sink)
        def sync_fn() -> str:
            return "result"

        result = sync_fn()

        assert result == "result"
        assert len(sink.events) == 1
        assert sink.events[0].event == "test.operation"
        assert sink.events[0].outcome == Outcome.SUCCESS
        assert sink.events[0].duration_ms >= 0

    def test_monitored_sync_callable_failure(self) -> None:
        """@monitored on sync callable emits FAILURE event on exception."""
        sink = CollectingSink()

        @monitored("test.operation", sink=sink)
        def sync_fn() -> None:
            raise ValueError("test error")

        with pytest.raises(ValueError, match="test error"):
            sync_fn()

        assert len(sink.events) == 1
        assert sink.events[0].event == "test.operation"
        assert sink.events[0].outcome == Outcome.FAILURE
        assert sink.events[0].is_failure

    def test_monitored_async_callable_success(self) -> None:
        """@monitored on async callable emits SUCCESS event."""
        sink = CollectingSink()

        @monitored("test.async_operation", sink=sink)
        async def async_fn() -> str:
            await asyncio.sleep(0.01)
            return "async_result"

        result = asyncio.run(async_fn())

        assert result == "async_result"
        assert len(sink.events) == 1
        assert sink.events[0].event == "test.async_operation"
        assert sink.events[0].outcome == Outcome.SUCCESS

    def test_monitored_async_callable_failure(self) -> None:
        """@monitored on async callable emits FAILURE event on exception."""
        sink = CollectingSink()

        @monitored("test.async_operation", sink=sink)
        async def async_fn() -> None:
            await asyncio.sleep(0.01)
            raise RuntimeError("async error")

        with pytest.raises(RuntimeError, match="async error"):
            asyncio.run(async_fn())

        assert len(sink.events) == 1
        assert sink.events[0].event == "test.async_operation"
        assert sink.events[0].outcome == Outcome.FAILURE

    def test_monitored_with_registry_sink(self) -> None:
        """@monitored resolves sink from registry when None."""
        registry_sink = CollectingSink()
        MonitorRegistry.set_default_sink(registry_sink)

        @monitored("test.registry_operation")
        def sync_fn() -> str:
            return "result"

        result = sync_fn()

        assert result == "result"
        assert len(registry_sink.events) == 1
        assert registry_sink.events[0].event == "test.registry_operation"

    def test_monitored_with_args_and_kwargs(self) -> None:
        """@monitored preserves function args and kwargs."""
        sink = CollectingSink()

        @monitored("test.with_args", sink=sink)
        def fn_with_args(a: int, b: str, c: float = 1.0) -> str:
            return f"{a}-{b}-{c}"

        result = fn_with_args(42, "test", c=3.5)

        assert result == "42-test-3.5"
        assert len(sink.events) == 1


class TestMonitoredOnClass:
    """@monitored on classes fans out to public methods."""

    def setup_method(self) -> None:
        """Clear registry before each test."""
        MonitorRegistry.clear_default_sink()

    def test_monitored_class_public_methods(self) -> None:
        """@monitored on class fans out to public methods."""
        sink = CollectingSink()

        @monitored("documents", sink=sink)
        @dataclass(frozen=True, slots=True)
        class DocumentService:
            """Document processing service."""

            name: str

            def process(self) -> str:
                return f"processing {self.name}"

            def analyze(self) -> str:
                return f"analyzing {self.name}"

            def _private_method(self) -> str:
                return "private"

        service = DocumentService(name="test.pdf")

        process_result = service.process()
        analyze_result = service.analyze()
        private_result = service._private_method()

        assert process_result == "processing test.pdf"
        assert analyze_result == "analyzing test.pdf"
        assert private_result == "private"
        assert len(sink.events) == 2
        assert sink.events[0].event == "documents.process"
        assert sink.events[1].event == "documents.analyze"

    def test_monitored_class_failure_on_method(self) -> None:
        """@monitored on class emits failure event from method exception."""
        sink = CollectingSink()

        @monitored("service", sink=sink)
        @dataclass(frozen=True, slots=True)
        class Service:
            """Test service."""

            fail: bool

            def execute(self) -> str:
                if self.fail:
                    raise RuntimeError("execution failed")
                return "success"

        service = Service(fail=True)

        with pytest.raises(RuntimeError, match="execution failed"):
            service.execute()

        assert len(sink.events) == 1
        assert sink.events[0].event == "service.execute"
        assert sink.events[0].is_failure

    def test_monitored_empty_class_raises(self) -> None:
        """@monitored on class with no public methods raises."""
        with pytest.raises(MonitoringDeclarationError):

            @monitored("empty")
            @dataclass(frozen=True, slots=True)
            class EmptyService:
                """Service with no public methods."""

                _private: str = ""

    def test_monitored_invalid_target_raises(self) -> None:
        """@monitored on invalid target raises."""
        with pytest.raises(MonitoringDeclarationError):
            monitored("test")(42)  # type: ignore


class TestMonitoredEdgeCases:
    """Edge cases and special scenarios."""

    def setup_method(self) -> None:
        """Clear registry before each test."""
        MonitorRegistry.clear_default_sink()

    def test_monitored_preserves_function_name(self) -> None:
        """@monitored preserves original function name."""

        @monitored("test")
        def my_function() -> str:
            return "result"

        assert my_function.__name__ == "my_function"

    def test_monitored_with_return_value_and_exception(self) -> None:
        """Multiple calls track separate success/failure events."""
        sink = CollectingSink()

        @monitored("test.toggle", sink=sink)
        def toggle_fn(should_fail: bool) -> str:
            if should_fail:
                raise ValueError("intentional")
            return "ok"

        result1 = toggle_fn(False)
        assert result1 == "ok"
        assert len(sink.events) == 1
        assert sink.events[0].outcome == Outcome.SUCCESS

        with pytest.raises(ValueError):
            toggle_fn(True)

        assert len(sink.events) == 2
        assert sink.events[1].outcome == Outcome.FAILURE

    def test_monitored_class_with_classmethod(self) -> None:
        """@monitored on class with classmethod includes it in public methods."""
        sink = CollectingSink()

        @monitored("factory", sink=sink)
        class FactoryService:
            """Service with classmethod."""

            @classmethod
            def create(cls) -> "FactoryService":
                """Factory method."""
                return cls()

        obj = FactoryService.create()
        assert obj is not None
        assert len(sink.events) == 1
        assert sink.events[0].event == "factory.create"
        assert sink.events[0].outcome == Outcome.SUCCESS

    def test_monitored_class_with_staticmethod(self) -> None:
        """@monitored on class with staticmethod includes it in public methods."""
        sink = CollectingSink()

        @monitored("utils", sink=sink)
        class UtilService:
            """Service with staticmethod."""

            @staticmethod
            def helper() -> str:
                """Helper function."""
                return "helper_result"

        result = UtilService.helper()
        assert result == "helper_result"
        assert len(sink.events) == 1
        assert sink.events[0].event == "utils.helper"
        assert sink.events[0].outcome == Outcome.SUCCESS
