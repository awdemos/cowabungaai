"""Tests for API Key CRUD operations."""

import pytest
from fastapi import HTTPException, status
from cowabunga_api.data.crud_api_key import CRUDAPIKey, APIKeyItem
from tests.mocks.mock_session import mock_session  # noqa: F401


@pytest.fixture
def mock_api_key_item():
    return APIKeyItem(
        name="Test Key",
        id="12345678-1234-1234-1234-1234567890ab",
        api_key="lfai_1234567890abcdef1234567890abcdef_1234",
        created_at=1700000000,
        expires_at=1700000000 + 2592000,
    )


@pytest.fixture
def crud_api_key(mock_session):
    return CRUDAPIKey(db=mock_session)


@pytest.mark.asyncio
async def test_crud_api_key_init_with_api_key_header(mock_session):
    """Test that CRUDAPIKey raises 401 when initialized with API key header."""
    mock_session.options.headers["x-custom-api-key"] = "test-key"
    with pytest.raises(HTTPException) as exc_info:
        CRUDAPIKey(db=mock_session)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_crud_api_key_create(crud_api_key, mock_api_key_item):
    """Test creating an API key."""
    result = await crud_api_key.create(mock_api_key_item)
    assert result is not None
    assert result.name == "mock-api-key"
    assert result.id == "12345678-1234-1234-1234-1234567890ab"


@pytest.mark.asyncio
async def test_crud_api_key_get(crud_api_key):
    """Test getting an API key by filters."""
    result = await crud_api_key.get(filters={"name": "Test Key"})
    assert result is not None
    assert "****" in result.api_key


@pytest.mark.asyncio
async def test_crud_api_key_list(crud_api_key):
    """Test listing API keys."""
    result = await crud_api_key.list()
    assert isinstance(result, list)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_crud_api_key_update(crud_api_key, mock_api_key_item):
    """Test updating an API key."""
    result = await crud_api_key.update(
        id_="12345678-1234-1234-1234-1234567890ab",
        object_=mock_api_key_item,
    )
    assert result is not None
    assert result.name == "mock-api-key"
