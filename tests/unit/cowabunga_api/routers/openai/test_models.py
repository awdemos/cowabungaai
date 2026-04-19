"""Tests for the OpenAI models router."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from cowabunga_api.routers.openai.models import router
from cowabunga_api.routers.supabase_session import init_supabase_client
from unittest.mock import patch, MagicMock, AsyncMock


def _client_with_auth_override():
    app = FastAPI()
    app.include_router(router)
    async def _mock_session(): return MagicMock()
    app.dependency_overrides[init_supabase_client] = _mock_session
    return TestClient(app)


@pytest.fixture
def mock_config():
    """Mock model configuration."""
    with patch("cowabunga_api.routers.openai.models.get_model_config") as mock:
        config = MagicMock()
        config.models = ["model1", "model2", "model3"]
        mock.return_value = config
        yield mock


def test_list_models(mock_config):
    """Test listing available models."""
    client = _client_with_auth_override()
    response = client.get("/openai/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 3
    assert data["data"][0]["id"] == "model1"
    assert data["data"][1]["id"] == "model2"
    assert data["data"][2]["id"] == "model3"


def test_list_models_empty(mock_config):
    """Test listing models when none are configured."""
    mock_config.return_value = MagicMock(models=[])
    client = _client_with_auth_override()
    response = client.get("/openai/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert data["data"] == []
