"""Tests for the health check router."""

import pytest
from fastapi.testclient import TestClient
from cowabunga_api.routers.health import router
from unittest.mock import patch, MagicMock


client = TestClient(router)


@pytest.fixture
def mock_psutil():
    """Mock psutil for health checks."""
    with patch("cowabunga_api.routers.health.psutil") as mock:
        mock.virtual_memory.return_value = MagicMock(
            total=16000000000,
            available=8000000000,
            percent=50.0,
            used=8000000000,
        )
        mock.cpu_percent.return_value = 25.0
        mock.disk_usage.return_value = MagicMock(percent=30.0)
        yield mock


@pytest.fixture
def mock_config():
    """Mock model configuration."""
    with patch("cowabunga_api.routers.health.get_model_config") as mock:
        config = MagicMock()
        config.configs = ["model1", "model2"]
        config.models = ["model1", "model2"]
        mock.return_value = config
        yield mock


def test_health_check(mock_psutil, mock_config):
    """Test the basic health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "0.14.0"
    assert "python_version" in data
    assert data["models_loaded"] == 2
    assert data["memory_usage"]["percent_used"] == 50.0
    assert data["cpu_usage"] == 25.0


def test_readiness_check(mock_psutil):
    """Test the readiness check endpoint."""
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["ready"] is True
    assert "timestamp" in data
    assert data["checks"]["database"] is True
    assert data["checks"]["models"] is True
    assert data["checks"]["memory"] is True
    assert data["checks"]["disk"] is True


def test_liveness_check():
    """Test the liveness check endpoint."""
    response = client.get("/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "timestamp" in data


def test_readiness_memory_high(mock_psutil):
    """Test readiness when memory usage is high."""
    mock_psutil.virtual_memory.return_value = MagicMock(percent=95.0)
    response = client.get("/ready")
    data = response.json()
    assert data["ready"] is False
    assert data["checks"]["memory"] is False


def test_readiness_disk_high(mock_psutil):
    """Test readiness when disk usage is high."""
    mock_psutil.disk_usage.return_value = MagicMock(percent=95.0)
    response = client.get("/ready")
    data = response.json()
    assert data["ready"] is False
    assert data["checks"]["disk"] is False
