"""
This module contains the database configuration and utilities.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import api_config, postgres_config

Base = declarative_base()

db_url = str(postgres_config.database_url)
print("postgres_config.database_url", postgres_config.database_url)

engine = create_engine(
    db_url,
    pool_pre_ping=True,
    echo=api_config.debug_enabled,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.

    Yields:
        Session: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
