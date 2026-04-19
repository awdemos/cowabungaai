"""Tests for audio typedef models."""

import pytest
from cowabunga_api.typedef.audio.audio_types import (
    CreateTranscriptionRequest,
    CreateTranscriptionResponse,
)


def test_create_transcription_request_defaults():
    """Test CreateTranscriptionRequest default values."""
    import io
    from fastapi import UploadFile
    mock_file = UploadFile(filename="test.wav", file=io.BytesIO(b"audio"))
    req = CreateTranscriptionRequest(
        file=mock_file,  # type: ignore
        model="whisper-1",
    )
    assert req.model == "whisper-1"
    assert req.language == ""
    assert req.prompt == ""
    assert req.response_format == "json"
    assert req.temperature == 1.0
    assert req.timestamp_granularities is None


def test_create_transcription_request_custom_values():
    """Test CreateTranscriptionRequest with custom values."""
    import io
    from fastapi import UploadFile
    mock_file = UploadFile(filename="test.wav", file=io.BytesIO(b"audio"))
    req = CreateTranscriptionRequest(
        file=mock_file,  # type: ignore
        model="whisper-1",
        language="en",
        prompt="test prompt",
        response_format="text",
        temperature=0.5,
    )
    assert req.language == "en"
    assert req.prompt == "test prompt"
    assert req.response_format == "text"
    assert req.temperature == 0.5


def test_create_transcription_response():
    """Test CreateTranscriptionResponse model."""
    resp = CreateTranscriptionResponse(text="Hello world")
    assert resp.text == "Hello world"
