"""Tests for Supabase client wrapper."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from cowabunga_api.data.database.supabase_client import SupabaseQueryBuilder, SupabaseAuthClient


@pytest.fixture
def mock_query():
    """Create a mock query chain."""
    query = MagicMock()
    query.select.return_value = query
    query.insert.return_value = query
    query.update.return_value = query
    query.delete.return_value = query
    query.eq.return_value = query
    query.execute = AsyncMock(return_value={"data": []})
    return query


@pytest.fixture
def mock_async_client():
    """Create a mock AsyncClient."""
    client = MagicMock()
    client.auth = MagicMock()
    client.auth.get_user = AsyncMock(return_value={"id": "user-123"})
    client.auth.set_session = AsyncMock()
    return client


def test_supabase_query_builder_select(mock_query):
    """Test query builder select."""
    builder = SupabaseQueryBuilder(mock_query)
    result = builder.select("*")
    assert result is builder
    mock_query.select.assert_called_once_with("*")


def test_supabase_query_builder_eq(mock_query):
    """Test query builder eq filter."""
    builder = SupabaseQueryBuilder(mock_query)
    result = builder.eq("id", "123")
    assert result is builder
    mock_query.eq.assert_called_once_with("id", "123")


@pytest.mark.asyncio
async def test_supabase_query_builder_execute(mock_query):
    """Test query builder execute."""
    builder = SupabaseQueryBuilder(mock_query)
    result = await builder.execute()
    mock_query.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_supabase_auth_client_get_user(mock_async_client):
    """Test auth client get_user without token."""
    auth = SupabaseAuthClient(mock_async_client)
    result = await auth.get_user()
    mock_async_client.auth.get_user.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_supabase_auth_client_get_user_with_token(mock_async_client):
    """Test auth client get_user with token."""
    auth = SupabaseAuthClient(mock_async_client)
    result = await auth.get_user(token="test-token")
    mock_async_client.auth.get_user.assert_awaited_once_with("test-token")


@pytest.mark.asyncio
async def test_supabase_auth_client_set_session(mock_async_client):
    """Test auth client set_session."""
    auth = SupabaseAuthClient(mock_async_client)
    await auth.set_session("access-123", "refresh-456")
    mock_async_client.auth.set_session.assert_awaited_once_with("access-123", "refresh-456")
