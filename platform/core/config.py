from typing import Literal, Optional

from pydantic import (
    BaseModel,
    PostgresDsn,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtConfig(BaseModel):
    """JWT configuration."""

    access_secret_key: str
    refresh_secret_key: str
    algorithm: str = "HS256"
    access_expiration: str = "1h"
    refresh_expiration: str = "7d"


class PostgresConfig(BaseModel):
    """Postgres configuration."""

    # Database
    server: str
    user: str
    password: str
    db: str
    port: str
    database_url: Optional[str] = None
    async_database_url: Optional[str] = None

    def build_database_url(self, async_mode: bool = False) -> str:
        scheme = "postgresql+asyncpg" if async_mode else "postgresql"
        return PostgresDsn.build(
            scheme=scheme,
            username=self.user,
            password=self.password,
            host=self.server,
            port=int(self.port),
            path=f"{self.db or ''}",
        ).unicode_string()

    @model_validator(mode="after")
    def assemble_db_connection(self):
        if not self.database_url:
            self.database_url = self.build_database_url()
        return self

    @model_validator(mode="after")
    def assemble_async_db_connection(self):
        if not self.async_database_url:
            self.async_database_url = self.build_database_url(async_mode=True)
        return self


class LogConfig(BaseModel):
    # Logging
    level: Literal[
        "TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"
    ] = "INFO"

    format: str = "console"
    path: str = "logs/platform.log"


class LivekitConfig(BaseModel):
    """Livekit configuration."""

    url: str
    api_key: str
    api_secret: str


class CorsConfig(BaseModel):
    """CORS configuration."""

    # CORS
    origins: list[str] | str

    @model_validator(mode="after")
    def assemble_cors_origins(self) -> "CorsConfig":
        """Assemble the CORS origins."""
        if self.origins:
            if isinstance(self.origins, str):
                self.origins = self.origins.split(",")
            elif isinstance(self.origins, list):
                self.origins = self.origins
        else:
            self.origins = ["*"]
        return self


class MinioConfig(BaseModel):
    """Minio configuration."""

    endpoint: str
    access_key: str
    secret_key: str
    bucket_name: str = "confera"


class EnvironmentConfig(BaseModel):
    """Environment configuration."""

    env: str

    @property
    def is_dev(self) -> bool:
        return self.env == "development" or self.env == "dev"

    @property
    def is_prod(self) -> bool:
        return self.env == "production" or self.env == "prod"

    @property
    def is_local(self) -> bool:
        return self.env == "local"

    @property
    def is_test(self) -> bool:
        return self.env == "test"

    @property
    def is_staging(self) -> bool:
        return self.env == "staging"

    @property
    def debug(self) -> bool:
        return self.is_dev or self.is_local


class ApiConfig(BaseModel):
    """API configuration."""

    prefix: str = "/api"
    # API
    version: str = "1.0.0"
    name: str = "API"
    description: str = "API for the application"

    debug: Optional[bool] = None

    # Environment
    env: Literal["development", "production", "local", "test", "staging"]

    @property
    def debug_enabled(self) -> bool:
        # if debug is explicitly set, give it priority
        if self.debug is not None:
            return self.debug

        return self.env in ["development", "local", "test", "staging"]

    @property
    def is_prod(self) -> bool:
        return self.env == "production"

    @property
    def is_dev(self) -> bool:
        return self.env == "development"


class WorkersConfig(BaseModel):
    """Workers configuration."""

    voip_api_key: str


class Config(BaseSettings):
    """Configuration for the api."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_max_split=1,
        env_nested_delimiter="_",
    )

    # Livekit
    livekit: LivekitConfig

    # LLMs
    openai_api_key: str

    # Minio
    minio: MinioConfig

    # Environment
    api: ApiConfig
    # JWT
    jwt: JwtConfig
    # Database
    postgres: PostgresConfig
    # Logging
    log: LogConfig
    # CORS
    cors: CorsConfig
    # Workers
    workers: WorkersConfig


# Load settings
config = Config()

postgres_config = config.postgres

jwt_config = config.jwt
api_config = config.api
cors_config = config.cors
log_config = config.log
minio_config = config.minio
workers_config = config.workers
