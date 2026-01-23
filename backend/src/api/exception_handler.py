import logging
from functools import wraps
from fastapi import HTTPException
from src.utils.classes import InvalidEntryError, UnauthorizedError, PermissionDeniedError, NotFoundError, AlreadyExistsError, AppError


ERROR_STATUS_MAP = {
    InvalidEntryError: 400,
    UnauthorizedError: 401,
    PermissionDeniedError: 403,
    NotFoundError: 404,
    AlreadyExistsError: 409,
}

logger = logging.getLogger(__name__)

def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AppError as e:
            status_code = ERROR_STATUS_MAP.get(type(e), 500)
            logger.warning(f"Caught {e.__class__.__name__}: {str(e)}")
            raise HTTPException(status_code=status_code, detail=str(e))
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail="Something went wrong")
    return wrapper