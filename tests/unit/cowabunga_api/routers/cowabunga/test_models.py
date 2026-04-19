"""Tests for the CowabungaAI models router."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from cowabunga_api.routers.cowabunga.models import router
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
    with patch("cowabunga_api.routers.cowabunga.models.get_model_config") as mock:
        config = MagicMock()
        config.models = ["model-a", "model-b"]
        config.configs = ["cfg1", "cfg2"]
        mock.return_value = config
        yield mock


def test_list_cowabunga_models(mock_config):
    """Test listing models via cowabunga endpoint."""
    mock_config.return_value = {"models": ["model-a", "model-b"]}
    client = _client_with_auth_override()
    response = client.get("/cowabunga/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
