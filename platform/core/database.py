"""
This module contains the database configuration and utilities.
"""

from typing import AsyncGenerator, Generator

from core.config import postgres_config
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

Base = declarative_base()


engine = create_engine(
    postgres_config.database_url,
    pool_pre_ping=True,
    echo=False,
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


# Async session
async_engine = create_async_engine(postgres_config.async_database_url)
async_session = AsyncSession(autocommit=False, autoflush=False, bind=async_engine)


class AsyncBase(AsyncAttrs, DeclarativeBase):
    pass


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as db:
        yield db
