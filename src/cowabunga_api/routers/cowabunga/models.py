from fastapi import APIRouter
from cowabunga_api.utils import get_model_config

router = APIRouter(prefix="/cowabunga/v1/models", tags=["cowabunga/models"])


@router.get("")
async def models():
    """List all the models."""
    return get_model_config()
