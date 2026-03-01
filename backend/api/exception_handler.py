import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from shared.utils import (
    AlreadyExistsError,
    AppError,
    InvalidEntryError,
    NotFoundError,
    PermissionDeniedError,
    UnauthorizedError,
)

ERROR_STATUS_MAP = {
    InvalidEntryError: 400,
    UnauthorizedError: 401,
    PermissionDeniedError: 403,
    NotFoundError: 404,
    AlreadyExistsError: 409,
}

COMMON_ERRORS = {
    400: {"description": "Invalid input"},
    401: {"description": "Unauthorized"},
    403: {"description": "Permission denied"},
    404: {"description": "Not found"},
    409: {"description": "Already exists"},
    429: {"description": "Too many requests"},
}

logger = logging.getLogger(__name__)


def responses_for(*codes: int):
    return {code: COMMON_ERRORS[code] for code in codes}


def error_handlers(app):
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        status_code = ERROR_STATUS_MAP.get(type(exc), 500)
        logger.warning(f"Caught {exc.__class__.__name__}: {str(exc)}")
        return JSONResponse(status_code=status_code, content={"detail": str(exc)})

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unexpected error: {str(exc)}")
        return JSONResponse(status_code=500, content={"detail": "Something went wrong"})
