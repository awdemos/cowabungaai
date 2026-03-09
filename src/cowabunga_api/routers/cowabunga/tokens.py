from fastapi import APIRouter
from cowabunga_api.utils import get_model_config
from cowabunga_api.backend.grpc_client import (
    count_tokens,
)

import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/cowabunga/v1/tokens", tags=["cowabunga/tokens"])


@router.post("/count")
async def count_tokens_route(text: str) -> int:
    config = get_model_config()
    logger.info(f"Model config: {config}")
    model = config.models["text-embeddings"]
    logger.info(f"Model: {model}")

    result = count_tokens(model, text)
    logger.info(f"Token count: {result}")
    return result
