"""Tests for Run CRUD operations."""

import pytest
from openai.types.beta.threads import Run
from cowabunga_api.data.crud_run import CRUDRun
from tests.mocks.mock_session import mock_session  # noqa: F401


@pytest.fixture
def crud_run(mock_session):
    return CRUDRun(db=mock_session)


@pytest.fixture
def mock_run():
    return Run(
        id="run_123",
        object="thread.run",
        created_at=1700000000,
        assistant_id="asst_123",
        thread_id="thread_123",
        status="completed",
        model="vllm",
        instructions="",
        tools=[],
    )


@pytest.mark.asyncio
async def test_crud_run_update(crud_run, mock_run):
    """Test updating a run."""
    result = await crud_run.update(id_="run_123", object_=mock_run)
    assert result is not None
