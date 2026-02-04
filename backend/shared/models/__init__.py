"""
shared.models

This package contains all ORM models for IT-JobScraper:
- User, JobListing, Skill, ScrapeReport, FavoritedJobListing
- RefreshToken, SavedFilter, SavedFilterSkill, EmailVerificationCode

All models are imported here for convenient access.
"""

from shared.models.job_listing import JobListing
from shared.models.skill import Skill
from shared.models.job_listing_skill import JobListingSkill
from shared.models.scrape_report import ScrapeReport
from shared.models.user import User
from shared.models.favorited_job_listing import FavoritedJobListing
from shared.models.refresh_token import RefreshToken
from shared.models.saved_filter import SavedFilter
from shared.models.saved_filter_skill import SavedFilterSkill
from shared.models.email_verification_code import EmailVerificationCode

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
