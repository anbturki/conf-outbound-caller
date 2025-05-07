from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.logging import setup_logging
from app.db.session import engine
from app.db.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    engine.dispose()
