"""gRPC client for OpenAI models."""

import time
from typing import Iterator, AsyncGenerator, Any, List
import grpc
from fastapi.responses import StreamingResponse

import cowabunga_sdk as sdk
from cowabunga_api.backend.helpers import recv_chat, recv_completion
from cowabunga_api.typedef.audio import (
    CreateTranscriptionResponse,
    CreateTranslationResponse,
)
from cowabunga_api.typedef.chat import (
    ChatChoice,
    ChatCompletionResponse,
    ChatMessage,
)
from cowabunga_api.typedef.completion import (
    CompletionChoice,
    CompletionResponse,
    FinishReason,
)
from cowabunga_api.typedef import Usage
from cowabunga_api.typedef.embeddings import (
    CreateEmbeddingResponse,
    EmbeddingResponseData,
)
from cowabunga_api.typedef.counting import (
    TokenCountResponse,
)
from cowabunga_api.utils.config import Model
from cowabunga_sdk.chat.chat_pb2 import (
    ChatCompletionResponse as ProtobufChatCompletionResponse,
)


async def stream_completion(model: Model, request: sdk.CompletionRequest):
    """Stream completion using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = sdk.CompletionStreamServiceStub(channel)
        stream = stub.CompleteStream(request)

        await stream.wait_for_connection()
        return StreamingResponse(
            recv_completion(stream, model.name), media_type="text/event-stream"
        )


async def completion(model: Model, request: sdk.CompletionRequest):
    """Complete using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = sdk.CompletionServiceStub(channel)
        response: sdk.CompletionResponse = await stub.Complete(request)
        finish_reason_enum = FinishReason(response.choices[0].finish_reason)

        return CompletionResponse(
            id=None,
            object="text_completion",
            model=model.name,
            created=int(time.time()),
            choices=[
                CompletionChoice(
                    index=0,
                    text=response.choices[0].text,
                    finish_reason=finish_reason_enum.to_finish_reason(),
                    logprobs=None,
                )
            ],
            usage=Usage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            ),
        )


async def stream_chat_completion(model: Model, request: sdk.ChatCompletionRequest):
    """Stream chat completion using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = sdk.ChatCompletionStreamServiceStub(channel)
        stream = stub.ChatCompleteStream(request)

        await stream.wait_for_connection()
        return StreamingResponse(
            recv_chat(stream, model.name), media_type="text/event-stream"
        )


async def stream_chat_completion_raw(
    model: Model, request: sdk.ChatCompletionRequest
) -> AsyncGenerator[ProtobufChatCompletionResponse, Any]:
    """Stream chat completion using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = sdk.ChatCompletionStreamServiceStub(channel)
        stream: grpc.aio.UnaryStreamCall[
            sdk.ChatCompletionRequest, sdk.ChatCompletionResponse
        ] = stub.ChatCompleteStream(request)

        await stream.wait_for_connection()

        async for response in stream:
            yield response


async def chat_completion(model: Model, request: sdk.ChatCompletionRequest):
    """Complete chat using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = sdk.ChatCompletionServiceStub(channel)
        response: sdk.ChatCompletionResponse = await stub.ChatComplete(request)
        finish_reason_enum = FinishReason(response.choices[0].finish_reason)

        return ChatCompletionResponse(
            model=model.name,
            choices=[
                ChatChoice(
                    index=0,
                    message=ChatMessage(
                        role=sdk.ChatRole.Name(
                            response.choices[0].chat_item.role
                        ).lower(),
                        content=response.choices[0].chat_item.content,
                    ),
                    finish_reason=finish_reason_enum.to_finish_reason(),
                )
            ],
            usage=Usage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            ),
        )


async def create_embeddings(model: Model, request: sdk.EmbeddingRequest):
    """Create embeddings using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = sdk.EmbeddingsServiceStub(channel)
        embeddings: List[EmbeddingResponseData] = []

        # Loop through inputs - 500 at a time
        for i in range(0, len(request.inputs), 500):
            request_embeddings = request.inputs[i : i + 500]

            range_request = sdk.EmbeddingRequest(inputs=request_embeddings)
            e: sdk.EmbeddingResponse = await stub.CreateEmbedding(range_request)
            if e and e.embeddings is not None:
                data = [
                    EmbeddingResponseData(
                        embedding=list(e.embeddings[i].embedding), index=i
                    )
                    for i in range(len(e.embeddings))
                ]
                embeddings.extend(data)

        return CreateEmbeddingResponse(
            data=embeddings,
            model=model.name,
            usage=Usage(prompt_tokens=0, total_tokens=0),
        )


async def create_transcription(model: Model, request: Iterator[sdk.AudioRequest]):
    """Transcribe audio using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = sdk.AudioStub(channel)
        response: sdk.AudioResponse = await stub.Transcribe(request)

        return CreateTranscriptionResponse(text=response.text)


async def create_translation(model: Model, request: Iterator[sdk.AudioRequest]):
    """Translate audio using the specified model."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = sdk.AudioStub(channel)
        response: sdk.AudioResponse = await stub.Translate(request)

        return CreateTranslationResponse(text=response.text)


async def create_token_count(model: Model, request: sdk.TokenCountRequest):
    """Count tokens using the specified model backend."""
    async with grpc.aio.insecure_channel(model.backend) as channel:
        stub = sdk.TokenCountServiceStub(channel)
        response: sdk.TokenCountResponse = await stub.CountTokens(request)

        return TokenCountResponse(
            token_count=response.count,
            model=model.name,
            text=request.text,
        )


def count_tokens(model, text):
    """Token count via the backend gRPC token-count endpoint; falls back to a
    conservative whitespace-based estimate if the backend is unavailable."""
    try:
        import asyncio
        return asyncio.get_event_loop().run_until_complete(
            create_token_count(model, sdk.TokenCountRequest(text=text))
        )
    except Exception:  # pragma: no cover - backend may not support token counting
        return max(1, len(text.split()) + 10)
