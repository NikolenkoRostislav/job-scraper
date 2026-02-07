"""
shared.utils.classes

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

from .enums import LogLevel, SeniorityLevel, SourceWebsite, JobOrder, LOG_LEVEL_PRIORITY
from .exceptions import (
    AppError,
    AlreadyExistsError,
    InvalidEntryError,
    NotFoundError,
    UnauthorizedError,
    PermissionDeniedError,
)

__all__ = [
    "JobOrder",
    "LogLevel",
    "SeniorityLevel",
    "SourceWebsite",
    "LOG_LEVEL_PRIORITY",
    "AppError",
    "AlreadyExistsError",
    "InvalidEntryError",
    "NotFoundError",
    "UnauthorizedError",
    "PermissionDeniedError",
]
