from functools import wraps
from fastapi import HTTPException
from src.utils.exceptions import *

def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except InvalidEntryError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except UnauthorizedError as e:
            raise HTTPException(status_code=401, detail=str(e))
        except PermissionDeniedError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except AlreadyExistsError as e:
            raise HTTPException(status_code=409, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    return wrapper