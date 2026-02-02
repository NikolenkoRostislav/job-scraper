"""
src.models

This package contains all ORM models for IT-JobScraper:
- User, JobListing, Skill, ScrapeReport, FavoritedJobListing
- RefreshToken, SavedFilter, SavedFilterSkill, EmailVerificationCode

All models are imported here for convenient access.
"""

from src.models.job_listing import JobListing
from src.models.skill import Skill
from src.models.job_listing_skill import JobListingSkill
from src.models.scrape_report import ScrapeReport
from src.models.user import User
from src.models.favorited_job_listing import FavoritedJobListing
from src.models.refresh_token import RefreshToken
from src.models.saved_filter import SavedFilter
from src.models.saved_filter_skill import SavedFilterSkill
from src.models.email_verification_code import EmailVerificationCode

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
