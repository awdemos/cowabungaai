"""This module contains the audio router for the OpenAI API."""

from itertools import chain
from typing import Annotated
from fastapi import APIRouter, Depends

from cowabunga_api.backend.grpc_client import create_transcription, create_translation
from cowabunga_api.backend.helpers import read_chunks
from cowabunga_api.typedef.audio import (
    CreateTranscriptionRequest,
    CreateTranscriptionResponse,
    CreateTranslationRequest,
)
from cowabunga_api.routers.database_session import Session
from cowabunga_api.utils import get_model_config, require_model_backend
from cowabunga_api.utils.config import Config
import cowabunga_sdk as sdk

router = APIRouter(prefix="/openai/v1/audio", tags=["openai/audio"])


@router.post("/transcriptions")
async def transcribe(
    session: Session,  # pylint: disable=unused-argument # required for authorizing endpoint
    model_config: Annotated[Config, Depends(get_model_config)],
    req: CreateTranscriptionRequest = Depends(CreateTranscriptionRequest.as_form),
) -> CreateTranscriptionResponse:
    """Create a transcription from the given audio file."""
    model = require_model_backend(model_config, req.model)

    # Create a request that contains the metadata for the AudioRequest
    audio_metadata = sdk.AudioMetadata(
        prompt=req.prompt, temperature=req.temperature, inputlanguage=req.language
    )
    audio_metadata_request = sdk.AudioRequest(metadata=audio_metadata)

    # Read the file and get an iterator of all the data chunks
    chunk_iterator = read_chunks(req.file.file, 1024)

    # combine our metadata and chunk_data iterators
    request_iterator = chain((audio_metadata_request,), chunk_iterator)

    return await create_transcription(model, request_iterator)


@router.post("/translations")
async def translate(
    session: Session,
    model_config: Annotated[Config, Depends(get_model_config)],
    req: CreateTranslationRequest = Depends(CreateTranslationRequest.as_form),
) -> CreateTranscriptionResponse:
    """Create a translation to english from the given audio file."""
    model = require_model_backend(model_config, req.model)

    # Create a request that contains the metadata for the AudioRequest
    audio_metadata = sdk.AudioMetadata(prompt=req.prompt, temperature=req.temperature)
    audio_metadata_request = sdk.AudioRequest(metadata=audio_metadata)

    # Read the file and get an iterator of all the data chunks
    chunk_iterator = read_chunks(req.file.file, 1024)

    # combine our metadata and chunk_data iterators
    request_iterator = chain((audio_metadata_request,), chunk_iterator)

    return await create_translation(model, request_iterator)
