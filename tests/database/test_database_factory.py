"""Tests for database factory."""

import pytest
import os
from unittest.mock import AsyncMock, patch, MagicMock
from cowabunga_api.utils.database_factory import (
    create_database_client,
    get_session,
)
from cowabunga_api.data.database import TursoClient


@pytest.mark.asyncio
class TestDatabaseFactory:
    """Test database factory functionality."""

    @patch('cowabunga_api.utils.database_factory.TursoClient.create', new_callable=AsyncMock)
    async def test_create_turso_client(self, mock_create):
        """Test creating Turso client from environment."""
        os.environ["DATABASE_TYPE"] = "turso"
        os.environ["TURSO_URL"] = "http://test-turso:8080"

        mock_client = MagicMock()
        mock_client.base_url = "http://test-turso:8080"
        mock_create.return_value = mock_client

        try:
            client = await create_database_client()

            assert client is mock_client
            assert client.base_url == "http://test-turso:8080"
            mock_create.assert_called_once_with(
                base_url="http://test-turso:8080",
                auth_token=None
            )
        finally:
            if "DATABASE_TYPE" in os.environ:
                del os.environ["DATABASE_TYPE"]
            if "TURSO_URL" in os.environ:
                del os.environ["TURSO_URL"]

    @patch('cowabunga_api.utils.database_factory.TursoClient.create', new_callable=AsyncMock)
    async def test_default_to_turso(self, mock_create):
        """Test that factory defaults to Turso if DATABASE_TYPE not set."""
        if "DATABASE_TYPE" in os.environ:
            del os.environ["DATABASE_TYPE"]

        os.environ["TURSO_URL"] = "http://test-default:8080"

        mock_client = MagicMock()
        mock_client.base_url = "http://test-default:8080"
        mock_create.return_value = mock_client

        try:
            client = await create_database_client()
            assert client is mock_client
            mock_create.assert_called_once_with(
                base_url="http://test-default:8080",
                auth_token=None
            )
        finally:
            if "TURSO_URL" in os.environ:
                del os.environ["TURSO_URL"]

    @patch('cowabunga_api.utils.database_factory.TursoClient.create', new_callable=AsyncMock)
    async def test_invalid_database_type(self, mock_create):
        """Test that factory ignores invalid database type and still creates Turso client."""
        os.environ["DATABASE_TYPE"] = "invalid"

        mock_client = MagicMock()
        mock_create.return_value = mock_client

        try:
            client = await create_database_client()
            assert client is mock_client
        finally:
            if "DATABASE_TYPE" in os.environ:
                del os.environ["DATABASE_TYPE"]

    @patch('cowabunga_api.utils.database_factory.TursoClient.create', new_callable=AsyncMock)
    async def test_missing_turso_config(self, mock_create):
        """Test error handling for missing Turso configuration."""
        os.environ["DATABASE_TYPE"] = "turso"
        # Don't set TURSO_URL - factory uses default
        if "TURSO_URL" in os.environ:
            del os.environ["TURSO_URL"]

        mock_create.side_effect = ValueError("TURSO_URL environment variable is required")

        with pytest.raises(ValueError, match="TURSO_URL"):
            await create_database_client()

        # Verify factory used default URL
        mock_create.assert_called_once_with(
            base_url="http://turso:8080",
            auth_token=None
        )

        if "DATABASE_TYPE" in os.environ:
            del os.environ["DATABASE_TYPE"]

    @patch('cowabunga_api.utils.database_factory.TursoClient.create', new_callable=AsyncMock)
    async def test_get_session_backward_compatibility(self, mock_create):
        """Test that get_session still works for backward compatibility."""
        os.environ["DATABASE_TYPE"] = "turso"
        os.environ["TURSO_URL"] = "http://test-compat:8080"

        mock_client = MagicMock()
        mock_client.base_url = "http://test-compat:8080"
        mock_create.return_value = mock_client

        try:
            client = await get_session()
            assert client is mock_client
        finally:
            if "DATABASE_TYPE" in os.environ:
                del os.environ["DATABASE_TYPE"]
            if "TURSO_URL" in os.environ:
                del os.environ["TURSO_URL"]
