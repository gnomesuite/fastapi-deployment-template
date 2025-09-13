"""
Configuration management using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # App configuration
    app_name: str = "Pet Store API"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database configuration
    database_url: Optional[str] = None
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: list = ["*"]
    
    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
_settings = None

def get_settings() -> Settings:
    """Get application settings (singleton pattern)"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
