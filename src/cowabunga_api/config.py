"""CowabungaAPI configuration with database backend support."""

import os
from typing import Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings with database backend configuration."""
    
    # Turso Configuration
    turso_database_path: str = Field(
        default="/data/cowabunga.db",
        description="Path to Turso/SQLite database file"
    )
    turso_url: Optional[str] = Field(
        default=None,
        description="Turso server URL (for remote Turso)"
    )
    turso_auth_token: Optional[str] = Field(
        default=None,
        description="Turso authentication token"
    )
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8080, description="API port")
    api_workers: int = Field(default=4, description="Number of API workers")
    
    # Model Configuration
    default_model: str = Field(default="synthia-7b", description="Default LLM model")
    max_tokens: int = Field(default=2048, description="Maximum tokens per response")
    temperature: float = Field(default=0.7, description="Model temperature")
    
    # Feature Flags
    enable_rag: bool = Field(default=True, description="Enable RAG functionality")
    enable_transcription: bool = Field(default=False, description="Enable transcription")
    enable_file_uploads: bool = Field(default=True, description="Enable file uploads")
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format (json or text)")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        # Support both old and new environment variable names
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            """Customize settings sources for backward compatibility."""
            return (init_settings, env_settings, file_secret_settings)
    
    def get_database_config(self) -> dict:
        """Get database configuration.
        
        Returns:
            Dictionary with database configuration
        """
        return {
            "type": "turso",
            "db_path": self.turso_database_path,
            "url": self.turso_url,
            "auth_token": self.turso_auth_token,
        }


# Global settings instance
settings = Settings()
