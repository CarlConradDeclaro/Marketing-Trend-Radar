from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Marketing Trend Radar"
    environment: str = "development"
    frontend_origin: str = "http://localhost:3000"
    gdelt_timeout_seconds: float = 30.0
    openai_api_key: str | None = None
    llm_model: str = "gpt-4o-mini"

    @field_validator("frontend_origin", mode="before")
    @classmethod
    def strip_frontend_origin(cls, value: str) -> str:
        return value.rstrip("/")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
