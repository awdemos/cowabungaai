from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from cowabunga_api.routers.supabase_session import Session
from cowabunga_api.utils.config import Config
from cowabunga_api.utils import get_model_config
from cowabunga_api.typedef.counting import (
    TokenCountRequest,
    TokenCountResponse,
)
from cowabunga_api.backend.grpc_client import create_token_count
import cowabunga_sdk as lfai

router = APIRouter(prefix="/cowabunga/v1/count", tags=["cowabunga/count"])


@router.post("/tokens")
async def tokens(
    session: Session,
    model_config: Annotated[Config, Depends(get_model_config)],
    request: TokenCountRequest,
) -> TokenCountResponse:
    model = model_config.get_model_backend(request.model)

    if not model:
        raise HTTPException(
            status_code=404, detail=f"Model '{request.model}' not found"
        )

    try:
        return await create_token_count(
            model, lfai.TokenCountRequest(text=request.text)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting tokens: {str(e)}")
