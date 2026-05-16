"""Health check endpoints for the CowabungaAI API."""

from fastapi import APIRouter
from pydantic import BaseModel
import psutil
import sys
from datetime import datetime
from cowabunga_api.utils import get_model_config
from cowabunga_api.utils.database_factory import get_database_client

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    timestamp: str
    version: str
    python_version: str
    memory_usage: dict
    cpu_usage: float
    models_loaded: int


class ReadinessResponse(BaseModel):
    """Readiness check response model."""

    ready: bool
    timestamp: str
    checks: dict


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint."""
    memory = psutil.virtual_memory()

    # Get model configuration
    config = get_model_config()
    models_loaded = len(config.configs) if config.configs else 0

    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="0.14.0",
        python_version=sys.version,
        memory_usage={
            "total": memory.total,
            "available": memory.available,
            "percent_used": memory.percent,
            "used": memory.used,
        },
        cpu_usage=psutil.cpu_percent(interval=1),
        models_loaded=models_loaded,
    )


@router.get("/ready", response_model=ReadinessResponse)
async def readiness_check():
    """Readiness check endpoint."""
    db_healthy = False
    try:
        db = await get_database_client()
        db_healthy = await db.health_check()
    except Exception:
        db_healthy = False

    models_healthy = False
    try:
        config = get_model_config()
        models_healthy = len(config.configs) > 0
    except Exception:
        models_healthy = False

    checks = {
        "database": db_healthy,
        "models": models_healthy,
        "memory": psutil.virtual_memory().percent < 90,
        "disk": psutil.disk_usage("/").percent < 90,
    }

    all_ready = all(checks.values())

    return ReadinessResponse(
        ready=all_ready, timestamp=datetime.utcnow().isoformat(), checks=checks
    )


@router.get("/live")
async def liveness_check():
    """Liveness check endpoint."""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}
