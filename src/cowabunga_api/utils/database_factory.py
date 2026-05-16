"""Database client factory for creating appropriate database backend."""

import os
from cowabunga_api.data.database import DatabaseClient, TursoClient


async def create_database_client() -> DatabaseClient:
    """Factory function to create database client based on environment.

    Creates a Turso client using environment variables.

    Returns:
        DatabaseClient instance (TursoClient)

    Raises:
        ValueError: If required environment variables are missing
    """
    # Turso/libSQL HTTP API configuration
    turso_url = os.getenv("TURSO_URL", "http://turso:8080")
    turso_auth_token = os.getenv("TURSO_AUTH_TOKEN")

    return await TursoClient.create(base_url=turso_url, auth_token=turso_auth_token)


# Backward compatibility alias
async def get_session() -> DatabaseClient:
    """Get database session (backward compatibility).

    Returns:
        DatabaseClient instance
    """
    return await create_database_client()
