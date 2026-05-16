"""Tests for database factory."""

import pytest
import os
from unittest.mock import AsyncMock, patch
from cowabunga_api.utils.database_factory import (
    create_database_client,
    get_session,
    DatabaseType
)
from cowabunga_api.data.database import TursoClient


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
    
    async def test_default_to_turso(self):
        """Test that factory defaults to Turso if DATABASE_TYPE not set."""
        # Ensure DATABASE_TYPE is not set
        if "DATABASE_TYPE" in os.environ:
            del os.environ["DATABASE_TYPE"]
        
        os.environ["TURSO_DATABASE_PATH"] = "/tmp/test_default.db"
        
        try:
            client = await create_database_client()
            assert isinstance(client, TursoClient)
        finally:
            del os.environ["TURSO_DATABASE_PATH"]
    
    async def test_invalid_database_type(self):
        """Test error handling for invalid database type."""
        os.environ["DATABASE_TYPE"] = "invalid"
        
        with pytest.raises(ValueError, match="Unknown DATABASE_TYPE"):
            await create_database_client()
        
        del os.environ["DATABASE_TYPE"]
    
    async def test_missing_turso_config(self):
        """Test error handling for missing Turso configuration."""
        os.environ["DATABASE_TYPE"] = "turso"
        # Don't set TURSO_DATABASE_PATH
        
        with pytest.raises(ValueError, match="TURSO_DATABASE_PATH"):
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
