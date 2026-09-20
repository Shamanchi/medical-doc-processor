"""Configuration settings."""
from functools import lru_cache
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    app_name: str = "Medical Document Processor"
    app_version: str = "0.1.0"
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=True, alias="DEBUG")
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"

    cors_origins: str = "*"
    @property
    def cors_origins_list(self) -> List[str]:
        return ["*"] if self.cors_origins == "*" else [o.strip() for o in self.cors_origins.split(",")]

    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    openai_base_url: str = Field(default="https://api.openai.com/v1", alias="OPENAI_BASE_URL")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")

    spacy_model: str = Field(default="en_core_web_sm", alias="SPACY_MODEL")
    medical_ner_model: str = Field(default="d4data/biomedical-ner-all", alias="MEDICAL_NER_MODEL")

    terminology_cache_ttl: int = Field(default=86400, alias="TERMINOLOGY_CACHE_TTL")
    validation_strict: bool = Field(default=True, alias="VALIDATION_STRICT")

    database_url: str = Field(default="sqlite:///./data.db", alias="DATABASE_URL")

    @field_validator("app_env")
    @classmethod
    def validate_app_env(cls, v: str) -> str:
        if v not in ["development", "staging", "production", "test"]:
            raise ValueError("APP_ENV must be one of development, staging, production, test")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        if v.upper() not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("LOG_LEVEL must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL")
        return v.upper()


@lru_cache
def get_settings() -> Settings:
    return Settings()