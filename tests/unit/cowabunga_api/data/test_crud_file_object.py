"""Tests for FileObject CRUD operations."""

import pytest
from openai.types import FileObject
from cowabunga_api.data.crud_file_object import CRUDFileObject, FilterFileObject
from tests.mocks.mock_session import mock_session  # noqa: F401


@pytest.fixture
def crud_file_object(mock_session):
    return CRUDFileObject(db=mock_session)


@pytest.fixture
def filter_file_object():
    return FilterFileObject(id="file-123")


@pytest.mark.asyncio
async def test_crud_file_object_get(crud_file_object, filter_file_object):
    """Test getting a file object by filter."""
    result = await crud_file_object.get(filters=filter_file_object)
    assert result is not None


@pytest.mark.asyncio
async def test_crud_file_object_list(crud_file_object, filter_file_object):
    """Test listing file objects."""
    result = await crud_file_object.list(filters=filter_file_object)
    assert isinstance(result, list)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_crud_file_object_delete(crud_file_object, filter_file_object):
    """Test deleting a file object."""
    result = await crud_file_object.delete(filters=filter_file_object)
    assert result is True
