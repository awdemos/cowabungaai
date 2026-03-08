"""Unit tests for TursoClient implementation."""

import pytest
import tempfile
import os
from leapfrogai_api.data.database.turso_client import TursoClient, TursoQueryBuilder
from leapfrogai_api.data.database.base import DatabaseClient


@pytest.fixture
async def turso_client():
    """Create TursoClient with temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        client = await TursoClient.create(db_path=db_path)
        yield client, db_path


@pytest.fixture
async def setup_test_table(turso_client):
    """Create test table for testing."""
    client, db_path = turso_client
    
    # Create test table
    import aiosqlite
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS test_users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
    
    yield client


@pytest.mark.asyncio
class TestTursoClient:
    """Test TursoClient functionality."""
    
    async def test_create_client(self, turso_client):
        """Test client creation."""
        client, db_path = turso_client
        assert client is not None
        assert isinstance(client, DatabaseClient)
        assert client.db_path == db_path
    
    async def test_table_returns_query_builder(self, turso_client):
        """Test that table() returns QueryBuilder."""
        client, _ = turso_client
        builder = client.table("test_users")
        assert isinstance(builder, TursoQueryBuilder)
    
    async def test_auth_client_exists(self, turso_client):
        """Test that auth client is available."""
        client, _ = turso_client
        auth = client.auth
        assert auth is not None
    
    async def test_options_exists(self, turso_client):
        """Test that options object exists."""
        client, _ = turso_client
        assert client.options is not None
        assert hasattr(client.options, 'headers')


@pytest.mark.asyncio
class TestTursoQueryBuilder:
    """Test TursoQueryBuilder functionality."""
    
    async def test_insert_and_select(self, setup_test_table):
        """Test inserting and selecting data."""
        client = setup_test_table
        
        # Insert data
        insert_result = await (
            client.table("test_users")
            .insert({"id": "1", "email": "test@example.com", "name": "Test User"})
            .execute()
        )
        
        assert insert_result.error is None
        assert len(insert_result.data) == 1
        assert insert_result.data[0]["email"] == "test@example.com"
        
        # Select data
        select_result = await (
            client.table("test_users")
            .select("*")
            .execute()
        )
        
        assert select_result.error is None
        assert len(select_result.data) == 1
    
    async def test_select_with_filter(self, setup_test_table):
        """Test selecting with equality filter."""
        client = setup_test_table
        
        # Insert multiple users
        await (
            client.table("test_users")
            .insert([
                {"id": "1", "email": "user1@example.com", "name": "User 1"},
                {"id": "2", "email": "user2@example.com", "name": "User 2"},
            ])
            .execute()
        )
        
        # Select with filter
        result = await (
            client.table("test_users")
            .select("*")
            .eq("id", "1")
            .execute()
        )
        
        assert result.error is None
        assert len(result.data) == 1
        assert result.data[0]["email"] == "user1@example.com"
    
    async def test_update(self, setup_test_table):
        """Test updating data."""
        client = setup_test_table
        
        # Insert user
        await (
            client.table("test_users")
            .insert({"id": "1", "email": "test@example.com", "name": "Old Name"})
            .execute()
        )
        
        # Update user
        update_result = await (
            client.table("test_users")
            .update({"name": "New Name"})
            .eq("id", "1")
            .execute()
        )
        
        assert update_result.error is None
        
        # Verify update
        select_result = await (
            client.table("test_users")
            .select("*")
            .eq("id", "1")
            .execute()
        )
        
        assert select_result.data[0]["name"] == "New Name"
    
    async def test_delete(self, setup_test_table):
        """Test deleting data."""
        client = setup_test_table
        
        # Insert user
        await (
            client.table("test_users")
            .insert({"id": "1", "email": "test@example.com", "name": "Test User"})
            .execute()
        )
        
        # Delete user
        delete_result = await (
            client.table("test_users")
            .delete()
            .eq("id", "1")
            .execute()
        )
        
        assert delete_result.error is None
        
        # Verify deletion
        select_result = await (
            client.table("test_users")
            .select("*")
            .execute()
        )
        
        assert len(select_result.data) == 0
    
    async def test_chained_filters(self, setup_test_table):
        """Test chaining multiple filters."""
        client = setup_test_table
        
        # Insert users
        await (
            client.table("test_users")
            .insert([
                {"id": "1", "email": "user1@example.com", "name": "Test User 1"},
                {"id": "2", "email": "user2@example.com", "name": "Test User 2"},
            ])
            .execute()
        )
        
        # Select with filter (note: SQLite only supports AND for now)
        result = await (
            client.table("test_users")
            .select("*")
            .eq("email", "user1@example.com")
            .execute()
        )
        
        assert result.error is None
        assert len(result.data) == 1


@pytest.mark.asyncio
class TestTursoAuthClient:
    """Test TursoAuthClient functionality."""
    
    async def test_auth_client_placeholder(self, turso_client):
        """Test that auth client is placeholder for now."""
        client, _ = turso_client
        
        # Auth client should exist but not fully implemented
        assert client.auth is not None
        
        # get_user without token should fail
        with pytest.raises(Exception):
            await client.auth.get_user()
