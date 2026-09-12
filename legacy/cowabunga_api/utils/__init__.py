from fastapi import HTTPException

from cowabunga_api.typedef.models import Model
from cowabunga_api.utils.config import Config

config = Config()


def get_model_config():
    return config


def require_model_backend(model_config: Config, name: str) -> Model:
    """Return the configured backend for `name` or raise the standard 405."""
    model = model_config.get_model_backend(name)
    if model is None:
        raise HTTPException(
            status_code=405,
            detail=f"Model {name} not found. Currently supported models are {list(model_config.models.keys())}",
        )
    return model
