"""Abstract base class for database clients."""

from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class QueryBuilder(ABC):
    """Abstract query builder for database operations."""
    
    @abstractmethod
    def select(self, columns: str = "*") -> "QueryBuilder":
        """Select columns from table."""
        pass
    
    @abstractmethod
    def insert(self, data: dict | list[dict]) -> "QueryBuilder":
        """Insert data into table."""
        pass
    
    @abstractmethod
    def update(self, data: dict) -> "QueryBuilder":
        """Update data in table."""
        pass
    
    @abstractmethod
    def delete(self) -> "QueryBuilder":
        """Delete from table."""
        pass
    
    @abstractmethod
    def eq(self, column: str, value: Any) -> "QueryBuilder":
        """Add equality filter."""
        pass
    
    @abstractmethod
    async def execute(self) -> Any:
        """Execute the query."""
        pass


class AuthClient(ABC):
    """Abstract authentication client."""
    
    @abstractmethod
    async def get_user(self, token: str | None = None) -> Any:
        """Get current user."""
        pass
    
    @abstractmethod
    async def set_session(self, access_token: str, refresh_token: str) -> None:
        """Set session tokens."""
        pass


class DatabaseClient(ABC):
    """Abstract database client interface.
    
    This interface abstracts the database client to support multiple backends
    (Supabase, Turso, etc.) while maintaining a consistent API.
    """
    
    @abstractmethod
    def table(self, table_name: str) -> QueryBuilder:
        """Get a query builder for a table.
        
        Args:
            table_name: Name of the database table
            
        Returns:
            QueryBuilder instance for building queries
        """
        pass
    
    @property
    @abstractmethod
    def auth(self) -> AuthClient:
        """Get authentication client.
        
        Returns:
            AuthClient instance for authentication operations
        """
        pass
    
    @property
    @abstractmethod
    def options(self) -> Any:
        """Get client options.
        
        Returns:
            Client options object with headers attribute
        """
        pass
    
    @classmethod
    @abstractmethod
    async def create(cls, **kwargs) -> "DatabaseClient":
        """Factory method to create database client.
        
        Args:
            **kwargs: Database-specific configuration
            
        Returns:
            Configured database client instance
        """
        pass


class DatabaseConfig(BaseModel):
    """Base configuration for database clients."""
    
    database_type: str = "supabase"  # or "turso"
