"""OpenAI compliant models router."""

from fastapi import APIRouter
from cowabunga_api.typedef.models import (
    ModelResponse,
    ModelResponseModel,
)
from cowabunga_api.routers.supabase_session import Session
from cowabunga_api.utils import get_model_config
from cowabunga_api.utils.config import Config

router = APIRouter(prefix="/openai/v1/models", tags=["openai/models"])


@router.get("")
async def models(
    session: Session,  # pylint: disable=unused-argument # required for authorizing endpoint
) -> ModelResponse:
    """List all available models."""
    res = ModelResponse(data=[])
    model_config: Config = get_model_config()
    for model in model_config.models:
        m = ModelResponseModel(id=model)
        res.data.append(m)
    return res
