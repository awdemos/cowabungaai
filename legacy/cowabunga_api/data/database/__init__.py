"""Database abstraction layer for CowabungaAI.

This module provides a database-agnostic interface that supports
Turso (SQLite/libSQL) backend.
"""

from cowabunga_api.data.database.base import DatabaseClient
from cowabunga_api.data.database.turso_client import TursoClient

__all__ = ["DatabaseClient", "TursoClient"]
