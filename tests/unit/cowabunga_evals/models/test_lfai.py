"""Tests for the CowabungaAI DeepEval model."""

import pytest
from unittest.mock import patch, MagicMock
from cowabunga_evals.models.lfai import COWABUNGA_Model


@pytest.fixture
def mock_openai_client():
    with patch("cowabunga_evals.models.lfai.openai.OpenAI") as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


@pytest.fixture
def model(mock_openai_client):
    return COWABUNGA_Model(
        api_key="test-key",
        base_url="http://test/openai/v1",
        model="test-model",
    )


def test_model_init(mock_openai_client):
    """Test COWABUNGA_Model initialization."""
    m = COWABUNGA_Model(
        api_key="test-key",
        base_url="http://test/openai/v1",
        model="test-model",
    )
    assert m.model == "test-model"
    assert m.api_key == "test-key"
    assert m.base_url == "http://test/openai/v1"


def test_load_model(model):
    """Test load_model returns the model name."""
    assert model.load_model() == "test-model"


def test_get_model_name(model):
    """Test get_model_name returns formatted name."""
    assert model.get_model_name() == "CowabungaAI test-model"


def test_generate_strips_stop_sequence(mock_openai_client, model):
    """Test generate strips the stop sequence from response."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Hello world</s>"
    mock_openai_client.chat.completions.create.return_value = mock_response

    result = model.generate("Say hello")
    assert result == "Hello world"


def test_generate_samples(mock_openai_client, model):
    """Test generate_samples returns n responses."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Hello"
    mock_openai_client.chat.completions.create.return_value = mock_response

    results = model.generate_samples(n=3, prompt="Say hello")
    assert len(results) == 3
    assert all(r == "Hello" for r in results)
