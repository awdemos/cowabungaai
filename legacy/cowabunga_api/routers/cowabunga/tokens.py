from fastapi import APIRouter
from cowabunga_api.utils import get_model_config
from cowabunga_api.backend.grpc_client import create_token_count
from cowabunga_api.routers.database_session import Session
import cowabunga_sdk as sdk

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

    result = await create_token_count(model, sdk.TokenCountRequest(text=text))
    logger.info(f"Token count: {result}")
    return result.token_count
