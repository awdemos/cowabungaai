"""Supabase client wrapper implementing DatabaseClient interface."""

from typing import Any
from supabase import AClient as AsyncClient, acreate_client
from cowabunga_api.data.database.base import DatabaseClient, QueryBuilder, AuthClient


class SupabaseQueryBuilder(QueryBuilder):
    """Supabase query builder wrapper."""
    
    def __init__(self, query):
        """Initialize with Supabase query."""
        self._query = query
    
    def select(self, columns: str = "*") -> "SupabaseQueryBuilder":
        """Select columns from table."""
        self._query = self._query.select(columns)
        return self
    
    def insert(self, data: dict | list) -> "SupabaseQueryBuilder":
        """Insert data into table."""
        self._query = self._query.insert(data)
        return self
    
    def update(self, data: dict) -> "SupabaseQueryBuilder":
        """Update data in table."""
        self._query = self._query.update(data)
        return self
    
    def delete(self) -> "SupabaseQueryBuilder":
        """Delete from table."""
        self._query = self._query.delete()
        return self
    
    def eq(self, column: str, value: Any) -> "SupabaseQueryBuilder":
        """Add equality filter."""
        self._query = self._query.eq(column, value)
        return self
    
    async def execute(self) -> Any:
        """Execute the query."""
        return await self._query.execute()


class SupabaseAuthClient(AuthClient):
    """Supabase authentication client wrapper."""
    
    def __init__(self, client: AsyncClient):
        """Initialize with Supabase client."""
        self._client = client
    
    async def get_user(self, token: str | None = None) -> Any:
        """Get current user."""
        if token:
            return await self._client.auth.get_user(token)
        return await self._client.auth.get_user()
    
    async def set_session(self, access_token: str, refresh_token: str) -> None:
        """Set session tokens."""
        await self._client.auth.set_session(access_token, refresh_token)


class SupabaseClient(DatabaseClient):
    """Supabase database client wrapper.
    
    This class wraps the Supabase AsyncClient to implement the DatabaseClient
    interface, providing backward compatibility while enabling future database
    backend swapping.
    """
    
    def __init__(self, client: AsyncClient):
        """Initialize with Supabase client.
        
        Args:
            client: Supabase AsyncClient instance
        """
        self._client = client
        self._auth = SupabaseAuthClient(client)
    
    def table(self, table_name: str) -> SupabaseQueryBuilder:
        """Get a query builder for a table.
        
        Args:
            table_name: Name of the database table
            
        Returns:
            SupabaseQueryBuilder instance
        """
        query = self._client.table(table_name)
        return SupabaseQueryBuilder(query)
    
    @property
    def auth(self) -> SupabaseAuthClient:
        """Get authentication client.
        
        Returns:
            SupabaseAuthClient instance
        """
        return self._auth
    
    @property
    def options(self) -> Any:
        """Get client options.
        
        Returns:
            Supabase client options object
        """
        return self._client.options
    
    @classmethod
    async def create(cls, supabase_url: str, supabase_key: str, **kwargs) -> "SupabaseClient":
        """Factory method to create Supabase client.
        
        Args:
            supabase_url: Supabase project URL
            supabase_key: Supabase anonymous key
            **kwargs: Additional Supabase options
            
        Returns:
            Configured SupabaseClient instance
        """
        client = await acreate_client(supabase_url=supabase_url, supabase_key=supabase_key, **kwargs)
        return cls(client)
