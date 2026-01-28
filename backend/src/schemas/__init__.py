"""
src.schemas

This package contains all Pydantic schemas for IT-JobScraper, including:

- Job schemas: JobBase, JobDetailed, JobFilters, JobListResponse, JobCreate
- Skill schemas: SkillBase, SkillDetailResponse, SkillListResponse
- User schemas: UserBase, UserCreateBase, UserCreateWithEmail, UserCreateWithGmail
- Token schemas: Token, Tokens
- Misc schemas: DateRange, WebsiteStats, ScrapeReport, LogEntry, SendEmail, Email

All schemas are imported here for convenient access across the backend.
"""

from src.schemas.job import JobBase, JobDetailed, JobFilters, JobListResponse, JobCreate
from src.schemas.misc import DateRange, WebsiteStats, ScrapeReport, LogEntry, SendEmail, Email
from src.schemas.skill import SkillBase, SkillDetailResponse, SkillListResponse
from src.schemas.token import Token, Tokens
from src.schemas.user import UserBase, UserCreateBase, UserCreateWithEmail, UserCreateWithGmail

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
