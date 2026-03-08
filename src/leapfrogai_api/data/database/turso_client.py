"""Turso database client implementing DatabaseClient interface."""

import asyncio
import aiosqlite
from typing import Any, Optional
from dataclasses import dataclass
from leapfrogai_api.data.database.base import DatabaseClient, QueryBuilder, AuthClient


@dataclass
class TursoResult:
    """Result wrapper for Turso queries."""
    data: list[dict]
    error: Optional[str] = None


class TursoQueryBuilder(QueryBuilder):
    """Turso/SQLite query builder."""
    
    def __init__(self, db_path: str, table_name: str):
        """Initialize query builder.
        
        Args:
            db_path: Path to SQLite database
            table_name: Name of the table
        """
        self.db_path = db_path
        self.table_name = table_name
        self._columns = "*"
        self._filters = []
        self._data = None
        self._operation = "SELECT"  # SELECT, INSERT, UPDATE, DELETE
    
    def select(self, columns: str = "*") -> "TursoQueryBuilder":
        """Select columns from table."""
        self._columns = columns
        self._operation = "SELECT"
        return self
    
    def insert(self, data: dict | list) -> "TursoQueryBuilder":
        """Insert data into table."""
        self._data = data if isinstance(data, list) else [data]
        self._operation = "INSERT"
        return self
    
    def update(self, data: dict) -> "TursoQueryBuilder":
        """Update data in table."""
        self._data = data
        self._operation = "UPDATE"
        return self
    
    def delete(self) -> "TursoQueryBuilder":
        """Delete from table."""
        self._operation = "DELETE"
        return self
    
    def eq(self, column: str, value: Any) -> "TursoQueryBuilder":
        """Add equality filter."""
        self._filters.append((column, "=", value))
        return self
    
    async def execute(self) -> TursoResult:
        """Execute the query."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                
                if self._operation == "SELECT":
                    return await self._execute_select(db)
                elif self._operation == "INSERT":
                    return await self._execute_insert(db)
                elif self._operation == "UPDATE":
                    return await self._execute_update(db)
                elif self._operation == "DELETE":
                    return await self._execute_delete(db)
                else:
                    return TursoResult(data=[], error="Invalid operation")
        except Exception as e:
            return TursoResult(data=[], error=str(e))
    
    async def _execute_select(self, db) -> TursoResult:
        """Execute SELECT query."""
        sql = f"SELECT {self._columns} FROM {self.table_name}"
        params = []
        
        if self._filters:
            where_clauses = []
            for col, op, val in self._filters:
                where_clauses.append(f"{col} {op} ?")
                params.append(val)
            sql += " WHERE " + " AND ".join(where_clauses)
        
        async with db.execute(sql, params) as cursor:
            rows = await cursor.fetchall()
            data = [dict(row) for row in rows]
            return TursoResult(data=data)
    
    async def _execute_insert(self, db) -> TursoResult:
        """Execute INSERT query."""
        results = []
        for record in self._data:
            columns = ", ".join(record.keys())
            placeholders = ", ".join(["?" for _ in record])
            sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
            
            cursor = await db.execute(sql, list(record.values()))
            await db.commit()
            
            # Fetch the inserted row
            last_id = cursor.lastrowid
            async with db.execute(f"SELECT * FROM {self.table_name} WHERE rowid = ?", [last_id]) as cursor:
                row = await cursor.fetchone()
                if row:
                    results.append(dict(row))
        
        return TursoResult(data=results)
    
    async def _execute_update(self, db) -> TursoResult:
        """Execute UPDATE query."""
        set_clauses = [f"{col} = ?" for col in self._data.keys()]
        sql = f"UPDATE {self.table_name} SET {', '.join(set_clauses)}"
        params = list(self._data.values())
        
        if self._filters:
            where_clauses = []
            for col, op, val in self._filters:
                where_clauses.append(f"{col} {op} ?")
                params.append(val)
            sql += " WHERE " + " AND ".join(where_clauses)
        
        await db.execute(sql, params)
        await db.commit()
        
        # Fetch updated rows
        return await self._execute_select(db)
    
    async def _execute_delete(self, db) -> TursoResult:
        """Execute DELETE query."""
        # Fetch rows before deletion
        select_result = await self._execute_select(db)
        
        sql = f"DELETE FROM {self.table_name}"
        params = []
        
        if self._filters:
            where_clauses = []
            for col, op, val in self._filters:
                where_clauses.append(f"{col} {op} ?")
                params.append(val)
            sql += " WHERE " + " AND ".join(where_clauses)
        
        await db.execute(sql, params)
        await db.commit()
        
        return select_result


class TursoAuthClient(AuthClient):
    """Turso authentication client.
    
    Note: Turso doesn't have built-in auth like Supabase.
    This is a placeholder that integrates with Keycloak or custom JWT.
    """
    
    def __init__(self):
        """Initialize auth client."""
        self._current_user_id = None
        self._access_token = None
    
    async def get_user(self, token: str | None = None) -> Any:
        """Get current user.
        
        For Turso, we validate the JWT token and extract user info.
        This integrates with Keycloak (UDS) or custom auth.
        """
        from dataclasses import dataclass
        
        @dataclass
        class UserResponse:
            user: Any
        
        @dataclass
        class User:
            id: str
            email: str = ""
        
        # TODO: Implement JWT validation
        # For now, return placeholder
        if self._current_user_id:
            return UserResponse(user=User(id=self._current_user_id))
        
        # If using custom API key auth, extract from token
        if token and token.startswith("lfai_"):
            # Extract user_id from api_keys table
            return UserResponse(user=User(id="api-key-user"))
        
        raise Exception("No authenticated user")
    
    async def set_session(self, access_token: str, refresh_token: str) -> None:
        """Set session tokens."""
        self._access_token = access_token
        # TODO: Validate JWT and extract user_id


class TursoOptions:
    """Turso client options."""
    
    def __init__(self):
        """Initialize options."""
        self.headers = {}
        self.auto_refresh_token = False


class TursoClient(DatabaseClient):
    """Turso/libSQL database client.
    
    This class implements the DatabaseClient interface for Turso/SQLite,
    providing the same API as Supabase but with SQLite backend.
    """
    
    def __init__(self, db_path: str):
        """Initialize Turso client.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._auth = TursoAuthClient()
        self._options = TursoOptions()
    
    def table(self, table_name: str) -> TursoQueryBuilder:
        """Get a query builder for a table.
        
        Args:
            table_name: Name of the database table
            
        Returns:
            TursoQueryBuilder instance
        """
        return TursoQueryBuilder(self.db_path, table_name)
    
    @property
    def auth(self) -> TursoAuthClient:
        """Get authentication client.
        
        Returns:
            TursoAuthClient instance
        """
        return self._auth
    
    @property
    def options(self) -> TursoOptions:
        """Get client options.
        
        Returns:
            TursoOptions instance
        """
        return self._options
    
    @classmethod
    async def create(cls, db_path: str = "/data/cowabunga.db", **kwargs) -> "TursoClient":
        """Factory method to create Turso client.
        
        Args:
            db_path: Path to SQLite database
            **kwargs: Additional options (ignored for Turso)
            
        Returns:
            Configured TursoClient instance
        """
        # Ensure database file exists
        import os
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)
        
        # Create database if it doesn't exist
        async with aiosqlite.connect(db_path) as db:
            await db.execute("SELECT 1")
        
        return cls(db_path)
