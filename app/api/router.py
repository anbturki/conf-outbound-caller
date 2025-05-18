# Main API router
from fastapi import APIRouter, Depends

from .dependencies import get_current_user
from .health.routes import router as health_router
from .resources.assistant.routes import router as assistant_router
from .resources.auth.routes import router as auth_router
from .resources.category.routes import router as category_router
from .resources.document.routes import router as document_router
from .resources.user.routes import router as user_router

# Protected routes
protected_router = APIRouter(dependencies=[Depends(get_current_user)])

# Public routes
public_router = APIRouter()

# Include routers - Public
public_router.include_router(auth_router)
public_router.include_router(health_router)

# Include routers - Protected
protected_router.include_router(assistant_router)
protected_router.include_router(user_router)
protected_router.include_router(document_router)
protected_router.include_router(category_router)
