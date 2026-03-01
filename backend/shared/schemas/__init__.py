"""
shared.schemas

This package contains all Pydantic schemas for IT-JobScraper, including:

- Job schemas: JobBase, JobDetailed, JobFilters, JobListResponse, JobCreate
- Skill schemas: SkillBase, SkillDetailResponse, SkillListResponse
- User schemas: UserBase, UserCreateBase, UserCreateWithEmail, UserCreateWithGmail
- Token schemas: Token, Tokens
- Misc schemas: DateRange, WebsiteStats, ScrapeReport, LogEntry, SendEmail, Email

All schemas are imported here for convenient access across the backend.
"""

from .job import JobBase, JobDetailed, JobFilters, JobListResponse, JobCreate
from .misc import DateRange, WebsiteStats, ScrapeReport, LogEntry, Email
from .skill import SkillBase, SkillDetailResponse, SkillListResponse
from .token import Token, Tokens
from .user import UserBase, UserCreateBase, UserCreateWithEmail, UserCreateWithGmail

__all__ = [
    "JobBase",
    "JobDetailed",
    "JobFilters",
    "JobListResponse",
    "JobCreate",
    "DateRange",
    "WebsiteStats",
    "ScrapeReport",
    "LogEntry",
    "Email",
    "SkillBase",
    "SkillDetailResponse",
    "SkillListResponse",
    "Token",
    "Tokens",
    "UserBase",
    "UserCreateBase",
    "UserCreateWithEmail",
    "UserCreateWithGmail",
]
