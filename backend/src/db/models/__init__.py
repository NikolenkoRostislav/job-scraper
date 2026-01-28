"""
src.db.models

This package contains all ORM models for IT-JobScraper:
- User, JobListing, Skill, ScrapeReport, FavoritedJobListing
- RefreshToken, SavedFilter, SavedFilterSkill, EmailVerificationCode

All models are imported here for convenient access.
"""

from src.db.models.job_listing import JobListing
from src.db.models.skill import Skill
from src.db.models.job_listing_skill import JobListingSkill
from src.db.models.scrape_report import ScrapeReport
from src.db.models.user import User
from src.db.models.favorited_job_listing import FavoritedJobListing
from src.db.models.refresh_token import RefreshToken
from src.db.models.saved_filter import SavedFilter
from src.db.models.saved_filter_skill import SavedFilterSkill
from src.db.models.email_verification_code import EmailVerificationCode

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
