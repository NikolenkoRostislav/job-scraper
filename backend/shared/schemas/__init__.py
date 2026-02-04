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

from shared.schemas.job import JobBase, JobDetailed, JobFilters, JobListResponse, JobCreate
from shared.schemas.misc import DateRange, WebsiteStats, ScrapeReport, LogEntry, SendEmail, Email
from shared.schemas.skill import SkillBase, SkillDetailResponse, SkillListResponse
from shared.schemas.token import Token, Tokens
from shared.schemas.user import UserBase, UserCreateBase, UserCreateWithEmail, UserCreateWithGmail

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
    "SendEmail",
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
