"""Tests for models typedef module."""

import pytest
from cowabunga_api.typedef.models.model_types import Model, ModelResponseModel, ModelResponse


def test_model_creation():
    """Test Model class can be instantiated."""
    model = Model(name="test-model", backend="llama-cpp-python")
    assert model.name == "test-model"
    assert model.backend == "llama-cpp-python"


def test_model_with_capabilities():
    """Test Model class with capabilities."""
    model = Model(
        name="test-model",
        backend="llama-cpp-python",
        capabilities=["chat", "completion"],
    )
    assert model.capabilities == ["chat", "completion"]


def test_model_response_model():
    """Test ModelResponseModel defaults."""
    model = ModelResponseModel(id="my-model")
    assert model.id == "my-model"
    assert model.object == "model"
    assert model.created == 0
    assert model.owned_by == "cowabungaai"


def test_model_response():
    """Test ModelResponse can be created."""
    response = ModelResponse(
        data=[
            ModelResponseModel(id="model-1"),
            ModelResponseModel(id="model-2"),
        ]
    )
    assert len(response.data) == 2
    assert response.data[0].id == "model-1"
    assert response.data[1].id == "model-2"
