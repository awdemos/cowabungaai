"""Database client factory for creating appropriate database backend."""

import os
from enum import Enum
from leapfrogai_api.data.database import DatabaseClient, SupabaseClient, TursoClient


class DatabaseType(str, Enum):
    """Supported database backends."""

    SUPABASE = "supabase"
    TURSO = "turso"


async def create_database_client() -> DatabaseClient:
    """Factory function to create database client based on environment.

    Reads DATABASE_TYPE from environment and creates appropriate client.
    Falls back to Supabase if not specified.

    Returns:
        DatabaseClient instance (SupabaseClient or TursoClient)

    Raises:
        ValueError: If required environment variables are missing
    """
    db_type = os.getenv("DATABASE_TYPE", DatabaseType.SUPABASE.value).lower()

    if db_type == DatabaseType.TURSO.value:
        # Turso/libSQL HTTP API configuration
        turso_url = os.getenv("TURSO_URL", "http://turso:8080")
        turso_auth_token = os.getenv("TURSO_AUTH_TOKEN")
        return await TursoClient.create(base_url=turso_url, auth_token=turso_auth_token)

    elif db_type == DatabaseType.SUPABASE.value:
        # Supabase configuration
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_ANON_KEY must be set for Supabase backend"
            )

        return await SupabaseClient.create(
            supabase_url=supabase_url, supabase_key=supabase_key
        )

    else:
        raise ValueError(
            f"Unknown DATABASE_TYPE: {db_type}. "
            f"Supported types: {[t.value for t in DatabaseType]}"
        )


# Backward compatibility alias
async def get_session() -> DatabaseClient:
    """Get database session (backward compatibility).

    This function maintains compatibility with existing code
    that expects a Supabase-like session.

    Returns:
        DatabaseClient instance
    """
    return await create_database_client()
