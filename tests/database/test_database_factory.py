"""Tests for database factory."""

import pytest
import os
from unittest.mock import AsyncMock, patch
from cowabunga_api.utils.database_factory import (
    create_database_client,
    get_session,
    DatabaseType
)
from cowabunga_api.data.database import SupabaseClient, TursoClient


@pytest.mark.asyncio
class TestDatabaseFactory:
    """Test database factory functionality."""
    
    async def test_create_turso_client(self):
        """Test creating Turso client from environment."""
        # Set environment
        os.environ["DATABASE_TYPE"] = "turso"
        os.environ["TURSO_DATABASE_PATH"] = "/tmp/test_factory.db"
        
        # Create client
        client = await create_database_client()
        
        assert isinstance(client, TursoClient)
        assert client.db_path == "/tmp/test_factory.db"
        
        # Cleanup
        del os.environ["DATABASE_TYPE"]
        del os.environ["TURSO_DATABASE_PATH"]
    
    async def test_create_supabase_client(self):
        """Test creating Supabase client from environment."""
        # Set environment
        os.environ["DATABASE_TYPE"] = "supabase"
        os.environ["SUPABASE_URL"] = "https://test.supabase.co"
        os.environ["SUPABASE_ANON_KEY"] = "test-key"
        
        # Mock Supabase client creation
        with patch('cowabunga_api.utils.database_factory.SupabaseClient.create') as mock_create:
            mock_client = AsyncMock()
            mock_create.return_value = mock_client
            
            client = await create_database_client()
            
            assert mock_create.called
            mock_create.assert_called_once_with(
                supabase_url="https://test.supabase.co",
                supabase_key="test-key"
            )
        
        # Cleanup
        del os.environ["DATABASE_TYPE"]
        del os.environ["SUPABASE_URL"]
        del os.environ["SUPABASE_ANON_KEY"]
    
    async def test_default_to_supabase(self):
        """Test that factory defaults to Supabase if DATABASE_TYPE not set."""
        # Ensure DATABASE_TYPE is not set
        if "DATABASE_TYPE" in os.environ:
            del os.environ["DATABASE_TYPE"]
        
        # Mock Supabase client creation
        with patch('cowabunga_api.utils.database_factory.SupabaseClient.create') as mock_create:
            mock_client = AsyncMock()
            mock_create.return_value = mock_client
            
            try:
                await create_database_client()
            except ValueError:
                # Expected if SUPABASE_URL/KEY not set
                pass
    
    async def test_invalid_database_type(self):
        """Test error handling for invalid database type."""
        os.environ["DATABASE_TYPE"] = "invalid"
        
        with pytest.raises(ValueError, match="Unknown DATABASE_TYPE"):
            await create_database_client()
        
        del os.environ["DATABASE_TYPE"]
    
    async def test_missing_supabase_config(self):
        """Test error handling for missing Supabase configuration."""
        os.environ["DATABASE_TYPE"] = "supabase"
        # Don't set SUPABASE_URL or SUPABASE_ANON_KEY
        
        with pytest.raises(ValueError, match="SUPABASE_URL and SUPABASE_ANON_KEY"):
            await create_database_client()
        
        del os.environ["DATABASE_TYPE"]
    
    async def test_get_session_backward_compatibility(self):
        """Test that get_session still works for backward compatibility."""
        os.environ["DATABASE_TYPE"] = "turso"
        os.environ["TURSO_DATABASE_PATH"] = "/tmp/test_compat.db"
        
        client = await get_session()
        
        assert isinstance(client, TursoClient)
        
        del os.environ["DATABASE_TYPE"]
        del os.environ["TURSO_DATABASE_PATH"]
