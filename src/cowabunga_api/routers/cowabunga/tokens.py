from fastapi import APIRouter
from cowabunga_api.utils import get_model_config
from cowabunga_api.backend.grpc_client import (
    count_tokens,
)
from cowabunga_api.routers.supabase_session import Session

import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/cowabunga/v1/tokens", tags=["cowabunga/tokens"])


@router.post("/count")
async def count_tokens_route(
    text: str,
    session: Session,  # pylint: disable=unused-argument # required for authorizing endpoint
) -> int:
    config = get_model_config()
    logger.info(f"Model config: {config}")
    model = config.models["text-embeddings"]
    logger.info(f"Model: {model}")

    result = count_tokens(model, text)
    logger.info(f"Token count: {result}")
    return result
