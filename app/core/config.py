from typing import List, Literal, Optional

from pydantic import (
    AnyHttpUrl,
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
    access_expire_hours: int = 1
    refresh_expire_days: int = 7


class PostgresConfig(BaseModel):
    """Postgres configuration."""

    # Database
    server: str
    user: str
    password: str
    db: str
    port: str
    database_url: Optional[PostgresDsn] = None

    @model_validator(mode="after")
    def assemble_db_connection(self) -> "PostgresConfig":
        """Assemble the database connection string."""
        print(f"assemble_db_connection called with data={self}")
        if not self.database_url:
            self.database_url = PostgresDsn.build(
                scheme="postgresql",
                username=self.user,
                password=self.password,
                host=self.server,
                port=int(self.port),
                path=f"{self.db or ''}",
            )
        return self


class LogConfig(BaseModel):
    # Logging
    level: Literal[
        "TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"
    ] = "INFO"

    format: str = "console"


class CorsConfig(BaseModel):
    """CORS configuration."""

    # CORS
    origins: List[AnyHttpUrl] | str

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


class ApiConfig(BaseModel):
    """API configuration."""

    prefix: str = "/api"
    # API
    version: str = "1.0.0"
    name: str = "API"
    description: str = "API for the application"


class EnvironmentConfig(BaseModel):
    """Environment configuration."""

    env: str = "development"

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


class Config(BaseSettings):
    """Configuration for the api."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_max_split=1,
        env_nested_delimiter="_",
    )

    # Environment
    api: ApiConfig
    # JWT
    jwt: JwtConfig
    # Environment
    environment: EnvironmentConfig
    # Database
    postgres: PostgresConfig
    # Logging
    log: LogConfig
    # CORS
    cors: CorsConfig


# Load settings
config = Config()

postgres_config = config.postgres
print("postgres_config", config.postgres)
jwt_config = config.jwt
api_config = config.api
cors_config = config.cors
log_config = config.log
environment_config = config.environment
