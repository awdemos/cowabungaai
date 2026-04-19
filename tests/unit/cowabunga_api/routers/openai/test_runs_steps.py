"""Tests for the runs steps router."""

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from cowabunga_api.routers.openai.runs_steps import router
from tests.utils.router_utils import client_with_auth_override
from unittest.mock import patch, AsyncMock, MagicMock


@pytest.fixture
def mock_run():
    """Create a mock run object."""
    from openai.types.beta.threads import Run
    return Run(
        id="run_123",
        object="thread.run",
        created_at=1700000000,
        assistant_id="asst_123",
        thread_id="thread_123",
        status="requires_action",
        model="vllm",
        instructions="",
        tools=[],
        parallel_tool_calls=False,
    )


@pytest.fixture
def mock_crud_run(mock_run):
    """Mock CRUDRun for testing."""
    with patch("cowabunga_api.routers.openai.runs_steps.CRUDRun") as mock:
        instance = AsyncMock()
        instance.get = AsyncMock(return_value=mock_run)
        instance.update = AsyncMock(return_value=mock_run)
        mock.return_value = instance
        yield mock


def test_submit_tool_outputs(mock_crud_run, mock_run):
    """Test submitting tool outputs for a run."""
    client = client_with_auth_override(router)
    response = client.post(
        "/openai/v1/threads/thread-123/runs/run-456/submit_tool_outputs",
        json=[{"tool_call_id": "call-1", "output": "result"}],
    )
    assert response.status_code == 200


def test_submit_tool_outputs_run_not_found(mock_crud_run):
    """Test 404 when run is not found."""
    mock_crud_run.return_value.get = AsyncMock(return_value=None)
    client = client_with_auth_override(router)
    response = client.post(
        "/openai/v1/threads/thread-123/runs/run-456/submit_tool_outputs",
        json=[{"tool_call_id": "call-1", "output": "result"}],
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_submit_tool_outputs_wrong_status(mock_crud_run):
    """Test 400 when run is not in requires_action state."""
    run = MagicMock()
    run.status = "completed"
    mock_crud_run.return_value.get = AsyncMock(return_value=run)
    client = client_with_auth_override(router)
    response = client.post(
        "/openai/v1/threads/thread-123/runs/run-456/submit_tool_outputs",
        json=[{"tool_call_id": "call-1", "output": "result"}],
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_submit_tool_outputs_empty(mock_crud_run, mock_run):
    """Test 400 when tool_outputs is empty."""
    client = client_with_auth_override(router)
    response = client.post(
        "/openai/v1/threads/thread-123/runs/run-456/submit_tool_outputs",
        json=[],
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_submit_tool_outputs_missing_tool_call_id(mock_crud_run, mock_run):
    """Test 400 when tool output missing tool_call_id."""
    client = client_with_auth_override(router)
    response = client.post(
        "/openai/v1/threads/thread-123/runs/run-456/submit_tool_outputs",
        json=[{"output": "result"}],
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
