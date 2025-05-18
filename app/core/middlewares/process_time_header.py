from time import time

from fastapi import Request


async def add_process_time_header(request: Request, call_next):
    """
    Middleware to add process time header to the response.
    """
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
