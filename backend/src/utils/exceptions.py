class AppError(Exception):
    pass

class InvalidEntryError(AppError):
    pass

class UnauthorizedError(AppError):
    pass
    
class PermissionDeniedError(AppError):
    pass

class NotFoundError(AppError):
    pass

class AlreadyExistsError(AppError):
    pass 


__all__ = [
    "AppError",
    "InvalidEntryError",
    "UnauthorizedError",
    "PermissionDeniedError",
    "NotFoundError",
    "AlreadyExistsError"
]
