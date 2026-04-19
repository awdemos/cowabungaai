from fastapi import APIRouter
from cowabunga_api.utils import get_model_config
from cowabunga_api.routers.supabase_session import Session

router = APIRouter(prefix="/cowabunga/v1/models", tags=["cowabunga/models"])


@router.get("")
async def models(
    session: Session,  # pylint: disable=unused-argument # required for authorizing endpoint
):
    """List all the models."""
    return get_model_config()
