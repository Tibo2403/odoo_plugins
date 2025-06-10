import importlib
import pytest


@pytest.fixture(autouse=True)
def reset_registry():
    """Reset registry and id sequence before each test."""
    from base_plugin.models import base_model
    importlib.reload(base_model)
    base_model.BaseModel._registry = []
    base_model.BaseModel._id_seq = 1
    return base_model.BaseModel


def test_search_returns_matching_records(reset_registry):
    BaseModel = reset_registry
    rec1 = BaseModel(name="first")
    BaseModel(name="second")

    result = BaseModel.search([("name", "=", "first")])

    assert rec1 in result
    assert len(result) == 1


def test_search_excludes_non_matching(reset_registry):
    BaseModel = reset_registry
    BaseModel(name="foo")
    BaseModel(name="bar")

    result = BaseModel.search([("name", "=", "unknown")])

    assert result == []
