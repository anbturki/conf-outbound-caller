from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import AnyHttpUrl, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API
    API_PREFIX: str = "/api"
    # CORS
    CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = ["http://localhost:3000"]

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[Any]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return [str(i) for i in v]  # Convert AnyHttpUrl or other types to strings
        elif isinstance(v, str):
            return [v]
        raise ValueError(f"Invalid CORS origins: {v}")

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "confera"
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: Optional[PostgresDsn] = None

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        values = info.data
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=int(values.get("POSTGRES_PORT")),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Logging
    LOG_LEVEL: Literal[
        "TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"
    ] = "INFO"

    LOG_FORMAT: str = "console"

    @field_validator("LOG_FORMAT", mode="before")
    def set_log_format(cls, v: str, info: ValidationInfo) -> str:
        if v is not None:
            return v
        environment = info.data.get("ENVIRONMENT", "development")
        return "json" if environment == "production" else "console"

    LOG_PATH: str = "logs"


# Load settings
settings = Settings()
