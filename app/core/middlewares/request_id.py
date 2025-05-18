from time import time

from fastapi import Request


async def add_request_id_middleware(request: Request, call_next):
    """
    Middleware to add request ID to the request.
    """
    request_id = request.headers.get("X-Request-ID", f"req-{time()}")
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response
