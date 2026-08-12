from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NexusBI AI"
    environment: str = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    secret_key: SecretStr
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    database_url: str
    redis_url: str
    mongodb_url: str
    mongodb_database: str = "nexusbi"
    storage_backend: str = "local"
    local_storage_path: str = "/data/uploads"
    dataset_sync_max_bytes: int = 10 * 1024 * 1024
    dataset_preview_rows: int = 100
    connector_sync_interval_minutes: int = 60
    connector_connection_timeout_seconds: int = 15
    s3_bucket: str | None = None
    s3_endpoint_url: str | None = None
    s3_region: str = "us-east-1"
    s3_access_key_id: SecretStr | None = None
    s3_secret_access_key: SecretStr | None = None
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
