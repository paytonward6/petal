import pytest

from petal.registry import template_registry

pytest.fixture(autouse=True, scope="function")
def flush_registry():
    template_registry.unregister_all()

