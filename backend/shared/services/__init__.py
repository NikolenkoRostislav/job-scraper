"""
shared.services

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

from shared.services.scrape_report import ScrapeReportService
from shared.services.saved_filter import SavedFilterService
from shared.services.email import EmailService
from shared.services.skill import SkillService
from shared.services.stats import StatsService
from shared.services.auth import AuthService
from shared.services.user import UserService
from shared.services.job import JobService

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
