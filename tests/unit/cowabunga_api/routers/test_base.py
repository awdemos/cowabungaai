"""Tests for the base router."""

from fastapi.testclient import TestClient
from fastapi import FastAPI
from cowabunga_api.routers.base import router


def test_healthz():
    """Test the health check endpoint."""
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
