"""
src.services

This package contains all backend service classes for IT-JobScraper, including:

- ScrapeReportService: handles scrape reports and related operations
- SavedFilterService: manages user saved filters
- EmailService: handles email sending and verification codes
- SkillService: manages skills-related operations
- StatsService: handles website/job/log statistics
- AuthService: authentication logic
- UserService: user management, creation, and queries
- JobService: job listing creation, retrieval, favoriting/unfavoriting

All services are imported here for convenient access across the backend.
"""

from src.services.scrape_report import ScrapeReportService
from src.services.saved_filter import SavedFilterService
from src.services.email import EmailService
from src.services.skill import SkillService
from src.services.stats import StatsService
from src.services.auth import AuthService
from src.services.user import UserService
from src.services.job import JobService

__all__ = [
    "ScrapeReportService",
    "SavedFilterService",
    "EmailService",
    "SkillService",
    "StatsService",
    "AuthService",
    "UserService",
    "JobService",
]
