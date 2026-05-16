"""Shared utilities for router unit tests."""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock

from cowabunga_api.routers.database_session import init_database_client


async def _mock_init_database_client():
    """Return a mock database session for testing."""
    session = MagicMock()
    mock_user = MagicMock()
    mock_user.user = MagicMock()
    mock_user.user.id = "test-user-id"
    session.auth.get_user = AsyncMock(return_value=mock_user)
    session.options = MagicMock()
    session.options.headers = {}
    return session


def client_with_auth_override(router) -> TestClient:
    """Return a TestClient for *router* with the auth dependency overridden."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[init_database_client] = _mock_init_database_client
    return TestClient(app)
