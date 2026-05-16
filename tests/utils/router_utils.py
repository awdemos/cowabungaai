"""Shared utilities for router unit tests."""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock


async def _mock_session():
    return MagicMock()


def client_with_auth_override(router) -> TestClient:
    """Return a TestClient for *router* with the auth dependency overridden."""
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)
