"""Tests for the OpenAI audio router."""

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from cowabunga_api.routers.openai.audio import router
from unittest.mock import patch, MagicMock


client = TestClient(router)


@pytest.fixture
def mock_config():
    """Mock model configuration."""
    with patch("cowabunga_api.routers.openai.audio.get_model_config") as mock:
        config = MagicMock()
        config.models = {"whisper-1": "whisper-backend"}
        config.get_model_backend = MagicMock(return_value="whisper-backend")
        mock.return_value = config
        yield mock


def test_transcribe_model_not_found(mock_config):
    """Test 405 when model is not found for transcription."""
    mock_config.return_value.get_model_backend = MagicMock(return_value=None)
    with patch("cowabunga_api.routers.openai.audio.Session") as mock_session:
        mock_session.return_value = MagicMock()
        response = client.post("/openai/v1/audio/transcriptions")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_translate_model_not_found(mock_config):
    """Test 405 when model is not found for translation."""
    mock_config.return_value.get_model_backend = MagicMock(return_value=None)
    with patch("cowabunga_api.routers.openai.audio.Session") as mock_session:
        mock_session.return_value = MagicMock()
        response = client.post("/openai/v1/audio/translations")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
