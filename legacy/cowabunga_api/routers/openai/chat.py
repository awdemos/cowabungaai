"""OpenAI Chat API router."""

from typing import Annotated, AsyncGenerator, Any
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import cowabunga_sdk as sdk
from cowabunga_api.backend.grpc_client import (
    chat_completion,
    stream_chat_completion,
    stream_chat_completion_raw,
)
from cowabunga_api.backend.helpers import grpc_chat_role
from cowabunga_api.typedef.chat import ChatCompletionRequest, ChatCompletionResponse
from cowabunga_api.routers.database_session import Session
from cowabunga_api.utils import get_model_config, require_model_backend
from cowabunga_api.utils.config import Config
from cowabunga_sdk.chat.chat_pb2 import (
    ChatCompletionResponse as ProtobufChatCompletionResponse,
)

router = APIRouter(prefix="/openai/v1/chat", tags=["openai/chat"])


def build_chat_request(req: ChatCompletionRequest) -> sdk.ChatCompletionRequest:
    chat_items: list[sdk.ChatItem] = []
    for m in req.messages:
        chat_items.append(
            sdk.ChatItem(role=grpc_chat_role(m.role), content=m.content_as_str())
        )
    return sdk.ChatCompletionRequest(
        chat_items=chat_items,
        max_new_tokens=req.max_tokens,
        temperature=req.temperature,
    )


@router.post("/completions", response_model=None)
async def chat_complete(
    req: ChatCompletionRequest,
    model_config: Annotated[Config, Depends(get_model_config)],
    session: Session,  # pylint: disable=unused-argument # required for authorizing endpoint
) -> ChatCompletionResponse | StreamingResponse:
    """Complete a chat conversation with the given model."""

    model = require_model_backend(model_config, req.model)
    request = build_chat_request(req)

    if req.stream:
        return await stream_chat_completion(model, request)
    else:
        return await chat_completion(model, request)


async def chat_complete_stream_raw(
    req: ChatCompletionRequest,
    model_config: Annotated[Config, Depends(get_model_config)],
) -> AsyncGenerator[ProtobufChatCompletionResponse, Any]:
    """Complete a prompt with the given model."""
    model = require_model_backend(model_config, req.model)
    request = build_chat_request(req)

    async for response in stream_chat_completion_raw(model, request):
        yield response
