"""OpenAI completions router."""

from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from cowabunga_api.backend.grpc_client import (
    completion,
    stream_completion,
)
from cowabunga_api.typedef.completion import CompletionRequest, CompletionResponse
from cowabunga_api.routers.database_session import Session
from cowabunga_api.utils import get_model_config, require_model_backend
from cowabunga_api.utils.config import Config
import cowabunga_sdk as sdk

router = APIRouter(prefix="/openai/v1/completions", tags=["openai/completions"])


@router.post("", response_model=None)
async def complete(
    session: Session,  # pylint: disable=unused-argument # required for authorizing endpoint
    req: CompletionRequest,
    model_config: Annotated[Config, Depends(get_model_config)],
) -> CompletionResponse | StreamingResponse:
    """Complete a prompt with the given model."""
    model = require_model_backend(model_config, req.model)

    request = sdk.CompletionRequest(
        prompt=req.prompt,  # type: ignore
        max_new_tokens=req.max_tokens,
        temperature=req.temperature,
    )

    if req.stream:
        return await stream_completion(model, request)
    else:
        return await completion(model, request)
