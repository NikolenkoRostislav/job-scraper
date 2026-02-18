import logging
import time

from fastapi import Request, FastAPI


logger = logging.getLogger(__name__)


def timing_middleware(app: FastAPI):
    @app.middleware("http")
    async def middleware(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        if duration > 1.0:
            logger.warning(
                f"Slow request: {request.method} {request.url.path} took {duration:.2f}s"
            )
        elif duration > 0.5:
            logger.info(f"{request.method} {request.url.path} took {duration:.2f}s")

        response.headers["X-Process-Time"] = str(duration)
        return response
