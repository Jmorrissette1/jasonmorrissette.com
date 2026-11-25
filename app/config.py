"""Application configuration, loaded from environment variables."""

from functools import lru_cache
from typing import Literal, Self

from pydantic import HttpUrl, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed, validated settings. Every field can be overridden by an APP_* env var."""

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: Literal["development", "production"] = "development"
    base_url: HttpUrl = HttpUrl("http://127.0.0.1:8000")

    @model_validator(mode="after")
    def _require_https_in_production(self) -> Self:
        if self.environment == "production" and self.base_url.scheme != "https":
            raise ValueError("APP_BASE_URL must use https when APP_ENVIRONMENT=production")
        return self

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """Build Settings once per process and reuse it."""
    return Settings()