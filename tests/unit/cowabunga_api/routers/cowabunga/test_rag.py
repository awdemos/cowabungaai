"""Tests for the CowabungaAI RAG router."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from cowabunga_api.routers.cowabunga.rag import router
from cowabunga_api.routers.supabase_session import init_supabase_client
from unittest.mock import patch, MagicMock, AsyncMock


def _client_with_auth_override():
    app = FastAPI()
    app.include_router(router)
    async def _mock_session(): return MagicMock()
    app.dependency_overrides[init_supabase_client] = _mock_session
    return TestClient(app)


@pytest.fixture
def mock_config_instance():
    """Mock ConfigurationSingleton instance."""
    instance = MagicMock()
    instance.chunk_size = 1000
    instance.chunk_overlap = 200
    instance.top_k = 5
    with patch("cowabunga_api.routers.cowabunga.rag.ConfigurationSingleton") as mock:
        mock.get_instance.return_value = instance
        yield mock


def test_get_configuration(mock_config_instance):
    """Test retrieving RAG configuration."""
    client = _client_with_auth_override()
    response = client.get("/cowabunga/v1/rag/configure")
    assert response.status_code == 200


def test_patch_configuration(mock_config_instance):
    """Test updating RAG configuration."""
    client = _client_with_auth_override()
    response = client.patch(
        "/cowabunga/v1/rag/configure",
        json={"chunk_size": 500},
    )
    assert response.status_code == 200
