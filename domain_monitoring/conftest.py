"""Root conftest for domain-monitoring tests."""

from collections.abc import Generator

import pytest

from domain_monitoring.services.registry.registry_client import MonitorRegistry


@pytest.fixture(autouse=True)
def reset_registry() -> Generator[None, None, None]:
    """Reset registry between tests."""
    MonitorRegistry.clear_default_sink()
    yield
    MonitorRegistry.clear_default_sink()
