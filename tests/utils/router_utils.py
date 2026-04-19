"""Shared utilities for router unit tests."""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from cowabunga_api.routers.supabase_session import init_supabase_client
from unittest.mock import MagicMock


def client_with_auth_override(router) -> TestClient:
    """Return a TestClient for *router* with the auth dependency overridden."""
    app = FastAPI()
    app.include_router(router)

    async def _mock_session():
        return MagicMock()

    app.dependency_overrides[init_supabase_client] = _mock_session
    return TestClient(app)
