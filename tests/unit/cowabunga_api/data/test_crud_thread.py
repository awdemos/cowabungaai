"""Tests for Thread CRUD operations."""

import pytest
from openai.types.beta import Thread
from cowabunga_api.data.crud_thread import CRUDThread
from tests.mocks.mock_session import mock_session  # noqa: F401


@pytest.fixture
def crud_thread(mock_session):
    return CRUDThread(db=mock_session)


@pytest.mark.asyncio
async def test_crud_thread_get(crud_thread):
    """Test getting a thread by filters."""
    result = await crud_thread.get(filters={"id": "thread-123"})
    assert result is not None


@pytest.mark.asyncio
async def test_crud_thread_list(crud_thread):
    """Test listing threads."""
    result = await crud_thread.list()
    assert isinstance(result, list)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_crud_thread_delete(crud_thread):
    """Test deleting a thread."""
    result = await crud_thread.delete(filters={"id": "thread-123"})
    assert result is True
