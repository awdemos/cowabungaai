"""Tests for Message CRUD operations."""

import pytest
from openai.types.beta.threads import Message
from cowabunga_api.data.crud_message import CRUDMessage
from tests.mocks.mock_session import mock_session  # noqa: F401


@pytest.fixture
def crud_message(mock_session):
    return CRUDMessage(db=mock_session)


@pytest.mark.asyncio
async def test_crud_message_get(crud_message):
    """Test getting a message by filters."""
    result = await crud_message.get(filters={"id": "msg-123", "thread_id": "thread-123"})
    assert result is not None


@pytest.mark.asyncio
async def test_crud_message_list(crud_message):
    """Test listing messages."""
    result = await crud_message.list(filters={"thread_id": "thread-123"})
    assert isinstance(result, list)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_crud_message_delete(crud_message):
    """Test deleting a message."""
    result = await crud_message.delete(filters={"id": "msg-123", "thread_id": "thread-123"})
    assert result is True
