# setup confera project, middlewares, db, config, routes, run the app, etc

from api.router import protected_router, public_router
from common.schemas.error_responses import ErrorResponse
from core.config import config
from core.error_handlers import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from core.events import lifespan
from core.exceptions import AppException
from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware


class ConferaApp(FastAPI):
    def __init__(self):
        super().__init__(
            title="Confera Platform API",
            version="1.0.0",
            lifespan=lifespan,
            debug=config.api.debug_enabled,
            responses={
                status.HTTP_422_UNPROCESSABLE_ENTITY: {
                    "model": ErrorResponse,
                    "description": "Validation error",
                }
            },
        )
        self._set_routers()
        self._add_exception_handlers()
        self._add_middlewares()

    def _set_routers(self):
        self.include_router(public_router, prefix=config.api.prefix)
        self.include_router(protected_router, prefix=config.api.prefix)

    def _add_exception_handlers(self):
        self.add_exception_handler(RequestValidationError, validation_exception_handler)
        self.add_exception_handler(AppException, app_exception_handler)
        self.add_exception_handler(Exception, http_exception_handler)
        self.add_exception_handler(HTTPException, http_exception_handler)

    def _add_middlewares(self):
        self.add_middleware(
            CORSMiddleware,
            allow_origins=config.cors.origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        # self.middleware("http")(add_request_id_middleware)
        # self.middleware("http")(add_process_time_header)

    def run(self):
        import uvicorn

        if config.api.is_prod:
            uvicorn.run(self, host="0.0.0.0", port=8000)
        else:
            uvicorn.run(
                self,
                host="localhost",
                port=8000,
                reload=True,
                reload_dirs=["app"],
            )
