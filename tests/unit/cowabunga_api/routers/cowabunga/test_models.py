"""Tests for the CowabungaAI models router."""

import pytest
from fastapi.testclient import TestClient
from cowabunga_api.routers.cowabunga.models import router
from unittest.mock import patch, MagicMock


client = TestClient(router)


@pytest.fixture
def mock_config():
    """Mock model configuration."""
    with patch("cowabunga_api.routers.cowabunga.models.get_model_config") as mock:
        config = MagicMock()
        config.models = ["model-a", "model-b"]
        config.configs = ["cfg1", "cfg2"]
        mock.return_value = config
        yield mock


def test_list_cowabunga_models(mock_config):
    """Test listing models via cowabunga endpoint."""
    response = client.get("/cowabunga/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
