"""
src.utils.classes

This package contains utility classes for IT-JobScraper, including:

- Enums:
    - LogLevel: defines logging levels
    - SeniorityLevel: defines job seniority levels
    - LOG_LEVEL_PRIORITY: priority mapping for log levels

- Exceptions:
    - AppError: base application exception
    - AlreadyExistsError: raised when an entry already exists
    - InvalidEntryError: raised for invalid input
    - NotFoundError: raised when an entity is not found
    - UnauthorizedError: raised for unauthorized access
    - PermissionDeniedError: raised when access is forbidden
"""

from src.utils.classes.enums import LogLevel, SeniorityLevel, LOG_LEVEL_PRIORITY
from src.utils.classes.exceptions import (
    AppError,
    AlreadyExistsError,
    InvalidEntryError,
    NotFoundError,
    UnauthorizedError,
    PermissionDeniedError,
)

__all__ = [
    "LogLevel",
    "SeniorityLevel",
    "LOG_LEVEL_PRIORITY",
    "AppError",
    "AlreadyExistsError",
    "InvalidEntryError",
    "NotFoundError",
    "UnauthorizedError",
    "PermissionDeniedError",
]
