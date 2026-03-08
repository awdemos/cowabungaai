"""Database abstraction layer for CowabungaAI.

This module provides a database-agnostic interface that supports both
Supabase (PostgreSQL) and Turso (SQLite/libSQL) backends.
"""

from leapfrogai_api.data.database.base import DatabaseClient
from leapfrogai_api.data.database.supabase_client import SupabaseClient
from leapfrogai_api.data.database.turso_client import TursoClient

__all__ = ["DatabaseClient", "SupabaseClient", "TursoClient"]
