"""Tests for the OpenAI audio router."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from cowabunga_api.routers.openai.audio import router
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
    with patch("cowabunga_api.routers.openai.audio.get_model_config") as mock:
        config = MagicMock()
        config.models = {"whisper-1": "whisper-backend"}
        config.get_model_backend = MagicMock(return_value="whisper-backend")
        mock.return_value = config
        yield mock


def test_transcribe_model_not_found(mock_config):
    """Test 405 when model is not found for transcription."""
    mock_config.return_value.get_model_backend = MagicMock(return_value=None)
    client = _client_with_auth_override()
    response = client.post(
        "/openai/v1/audio/transcriptions",
        data={"model": "whisper-1"},
        files={"file": ("test.wav", b"audio", "audio/wav")},
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_translate_model_not_found(mock_config):
    """Test 405 when model is not found for translation."""
    mock_config.return_value.get_model_backend = MagicMock(return_value=None)
    client = _client_with_auth_override()
    response = client.post(
        "/openai/v1/audio/translations",
        data={"model": "whisper-1"},
        files={"file": ("test.wav", b"audio", "audio/wav")},
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
