"""Tests for VectorContent CRUD operations."""

import pytest
from cowabunga_api.data.crud_vector_content import CRUDVectorContent
from cowabunga_api.typedef.vectorstores import Vector
from tests.mocks.mock_session import mock_session  # noqa: F401


@pytest.fixture
def crud_vector_content(mock_session):
    return CRUDVectorContent(db=mock_session)


@pytest.fixture
def mock_vectors():
    return [
        Vector(
            id="vec-1",
            vector_store_id="vs-1",
            file_id="file-1",
            content="test content",
            metadata={"source": "test"},
            embedding=[0.1, 0.2, 0.3],
        )
    ]


@pytest.mark.asyncio
async def test_crud_vector_content_init(mock_session):
    """Test CRUDVectorContent initialization."""
    crud = CRUDVectorContent(db=mock_session)
    assert crud.table_name == "vector_content"


@pytest.mark.asyncio
async def test_string_to_float_list(crud_vector_content):
    """Test converting string representation of floats to list."""
    result = crud_vector_content.string_to_float_list("[0.1, 0.2, 0.3]")
    assert result == [0.1, 0.2, 0.3]


@pytest.mark.asyncio
async def test_string_to_float_list_empty(crud_vector_content):
    """Test converting empty string representation."""
    result = crud_vector_content.string_to_float_list("[]")
    assert result == []
