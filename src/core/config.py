"""Configuration management for MediaWiki AI Agent."""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings, validator


class MediaWikiSettings(BaseSettings):
    """MediaWiki connection settings."""
    url: str
    bot_user: str
    bot_password: str
    timeout: int = 30
    rate_limit_reads: float = 1.0  # requests per second
    rate_limit_edits: float = 0.2  # requests per second
    verify_ssl: bool = True

    class Config:
        env_prefix = "MEDIAWIKI_"
        case_sensitive = False


class LLMSettings(BaseSettings):
    """LLM configuration."""
    provider: str = "openai"  # openai, anthropic, local
    model: str = "gpt-4"
    api_key: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000

    class Config:
        env_prefix = "LLM_"
        case_sensitive = False


class VectorStoreSettings(BaseSettings):
    """Vector store configuration."""
    type: str = "faiss"  # faiss, pinecone, milvus
    dimension: int = 384
    metric: str = "cosine"

    class Config:
        env_prefix = "VECTOR_DB_"
        case_sensitive = False


class CacheSettings(BaseSettings):
    """Cache configuration."""
    backend: str = "memory"  # memory, redis
    ttl: int = 3600  # seconds
    max_size: int = 1000

    class Config:
        env_prefix = "CACHE_"
        case_sensitive = False


class Settings(BaseSettings):
    """Main settings class."""
    mediawiki: MediaWikiSettings = MediaWikiSettings()
    llm: LLMSettings = LLMSettings()
    vector_store: VectorStoreSettings = VectorStoreSettings()
    cache: CacheSettings = CacheSettings()
    
    log_level: str = "INFO"
    debug: bool = False

    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {v}")
        return v.upper()

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def project_root(self) -> Path:
        """Get project root directory."""
        return Path(__file__).parent.parent.parent


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()


# Global settings instance
settings = get_settings()
