"""
src.db

This package handles the database layer for IT-JobScraper, including:
- Database connection/session setup
- ORM models for users, jobs, skills, reports, tokens, and email verification
- Utilities for accessing the database

Modules:
- database: DB connection and session management
- models: ORM models for all entities
"""

from src.db.database import get_db

# Import models for convenience
from src.db.models import *

__all__ = [
    "get_db",
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
