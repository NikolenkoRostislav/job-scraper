"""
src.api.routes

This package contains all FastAPI route modules for IT-JobScraper:
- job: routes related to job listings
- skill: routes related to skills management
- user: routes related to user management
- auth: routes for authentication
- admin: routes for administrative actions and monitoring

All routers are exposed for easy inclusion in the main FastAPI app.
"""

from src.api.routes.job import router as job_router
from src.api.routes.skill import router as skill_router
from src.api.routes.user import router as user_router
from src.api.routes.auth import router as auth_router
from src.api.routes.admin import router as admin_router

__all__ = [
    "job_router",
    "skill_router",
    "user_router",
    "auth_router",
    "admin_router",
]
