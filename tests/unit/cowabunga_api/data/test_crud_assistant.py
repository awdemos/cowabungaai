"""Tests for Assistant CRUD operations."""

import pytest
from openai.types.beta import Assistant
from cowabunga_api.data.crud_assistant import CRUDAssistant, FilterAssistant
from tests.mocks.mock_session import mock_session  # noqa: F401


@pytest.fixture
def crud_assistant(mock_session):
    return CRUDAssistant(db=mock_session)


@pytest.fixture
def filter_assistant():
    return FilterAssistant(id="asst_123")


@pytest.mark.asyncio
async def test_crud_assistant_get(crud_assistant, filter_assistant):
    """Test getting an assistant by filter."""
    result = await crud_assistant.get(filters=filter_assistant)
    assert result is not None


@pytest.mark.asyncio
async def test_crud_assistant_get_no_filter(crud_assistant):
    """Test getting an assistant without filter."""
    result = await crud_assistant.get(filters=None)
    assert result is not None


@pytest.mark.asyncio
async def test_crud_assistant_list(crud_assistant, filter_assistant):
    """Test listing assistants."""
    result = await crud_assistant.list(filters=filter_assistant)
    assert isinstance(result, list)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_crud_assistant_delete(crud_assistant, filter_assistant):
    """Test deleting an assistant."""
    result = await crud_assistant.delete(filters=filter_assistant)
    assert result is True
