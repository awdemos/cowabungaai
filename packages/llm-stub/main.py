"""LLM backend for CowabungaAI: TensorZero-backed gRPC service on :50051.

Same cowabunga_sdk contract as the echo-stub (and llama-cpp-python backend),
but generation proxies to the TensorZero gateway's OpenAI-compatible
chat completions endpoint, streaming chunks back to the composer.
"""
import json
import logging
import os
import urllib.request
from typing import Any, AsyncGenerator

from cowabunga_sdk import BackendConfig
from cowabunga_sdk.llm import LLM, GenerationConfig

logging.basicConfig(
    level=os.getenv("COWABUNGA_LOG_LEVEL", logging.INFO),
    format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s",
)
logger = logging.getLogger(__name__)

TZ_BASE = os.getenv("TZ_OPENAI_BASE_URL", "http://tensorzero-gw:3000/openai/v1")
TZ_KEY = os.getenv("TZ_API_KEY", "")
TZ_MODEL = os.getenv("TZ_MODEL", "tensorzero::model_name::glm")


def _tz_call(prompt: str) -> str:
    body = json.dumps(
        {"model": TZ_MODEL, "messages": [{"role": "user", "content": prompt}], "stream": True}
    ).encode()
    req = urllib.request.Request(
        TZ_BASE + "/chat/completions",
        data=body,
        headers={"Authorization": "Bearer " + TZ_KEY, "Content-Type": "application/json"},
        method="POST",
    )
    text_parts: list[str] = []
    with urllib.request.urlopen(req) as resp:
        for raw in resp:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if not payload or payload == "[DONE]":
                continue
            try:
                chunk = json.loads(payload)
            except ValueError:
                continue
            for choice in chunk.get("choices", []):
                delta = choice.get("delta") or {}
                piece = delta.get("content") or (choice.get("message") or {}).get("content")
                if piece:
                    text_parts.append(piece)
    return "".join(text_parts)


@LLM
class Model:
    backend_config = BackendConfig()

    async def generate(
        self, prompt: str, config: GenerationConfig
    ) -> AsyncGenerator[str, Any]:
        logger.info("TZ generate called (prompt %d chars)", len(prompt))
        try:
            text = _tz_call(prompt)
        except Exception as exc:  # surface failure to composer, keep pod alive
            logger.exception("TensorZero call failed")
            text = "Backend error: %s" % exc
        for i in range(0, len(text), 24):
            yield text[i : i + 24]

    async def count_tokens(self, raw_text: str) -> int:
        return max(1, len(raw_text.split()))
