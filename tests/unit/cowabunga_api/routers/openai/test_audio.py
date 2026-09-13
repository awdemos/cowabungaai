"""Tests for the OpenAI audio router."""

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from cowabunga_api.routers.openai.audio import router
from tests.utils.router_utils import client_with_auth_override
from unittest.mock import patch, MagicMock


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
    client = client_with_auth_override(router)
    response = client.post(
        "/openai/v1/audio/transcriptions",
        data={"model": "whisper-1"},
        files={"file": ("test.wav", b"audio", "audio/wav")},
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_translate_model_not_found(mock_config):
    """Test 405 when model is not found for translation."""
    mock_config.return_value.get_model_backend = MagicMock(return_value=None)
    client = client_with_auth_override(router)
    response = client.post(
        "/openai/v1/audio/translations",
        data={"model": "whisper-1"},
        files={"file": ("test.wav", b"audio", "audio/wav")},
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
