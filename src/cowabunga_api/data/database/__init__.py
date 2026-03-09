"""Database abstraction layer for CowabungaAI.

This module provides a database-agnostic interface that supports both
Supabase (PostgreSQL) and Turso (SQLite/libSQL) backends.
"""

from cowabunga_api.data.database.base import DatabaseClient
from cowabunga_api.data.database.supabase_client import SupabaseClient
from cowabunga_api.data.database.turso_client import TursoClient

__all__ = ["DatabaseClient", "SupabaseClient", "TursoClient"]
