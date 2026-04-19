"""Tests for the CowabungaAI RAG router."""

import pytest
from fastapi.testclient import TestClient
from cowabunga_api.routers.cowabunga.rag import router
from unittest.mock import patch, MagicMock


client = TestClient(router)


@pytest.fixture
def mock_config_instance():
    """Mock ConfigurationSingleton instance."""
    instance = MagicMock()
    instance.__dict__ = {
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "top_k": 5,
    }
    with patch("cowabunga_api.routers.cowabunga.rag.ConfigurationSingleton") as mock:
        mock.get_instance.return_value = instance
        yield mock


def test_get_configuration(mock_config_instance):
    """Test retrieving RAG configuration."""
    with patch("cowabunga_api.routers.cowabunga.rag.Session") as mock_session:
        mock_session.return_value = MagicMock()
        response = client.get("/cowabunga/v1/rag/configure")
        assert response.status_code == 200


def test_patch_configuration(mock_config_instance):
    """Test updating RAG configuration."""
    with patch("cowabunga_api.routers.cowabunga.rag.Session") as mock_session:
        mock_session.return_value = MagicMock()
        response = client.patch(
            "/cowabunga/v1/rag/configure",
            json={"chunk_size": 500},
        )
        assert response.status_code == 200
