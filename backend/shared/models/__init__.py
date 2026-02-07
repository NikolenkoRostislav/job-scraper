"""
shared.models

This package contains all ORM models for IT-JobScraper:
- User, JobListing, Skill, ScrapeReport, FavoritedJobListing
- RefreshToken, SavedFilter, SavedFilterSkill, EmailVerificationCode

All models are imported here for convenient access.
"""

from .job_listing import JobListing
from .skill import Skill
from .job_listing_skill import JobListingSkill
from .scrape_report import ScrapeReport
from .user import User
from .favorited_job_listing import FavoritedJobListing
from .refresh_token import RefreshToken
from .saved_filter import SavedFilter
from .saved_filter_skill import SavedFilterSkill
from .email_verification_code import EmailVerificationCode

__all__ = [
    "JobListing",
    "Skill",
    "JobListingSkill",
    "ScrapeReport",
    "User",
    "FavoritedJobListing",
    "RefreshToken",
    "SavedFilter",
    "SavedFilterSkill",
    "EmailVerificationCode",
]
