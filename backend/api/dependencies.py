from typing import Annotated

from core.database import get_db
from core.oauth import oauth2_scheme
from core.security import decode_token
from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from shared.models import User
from shared.schemas import JobFilters
from shared.utils import (
    NotFoundError,
    PermissionDeniedError,
    SeniorityLevel,
    UnauthorizedError,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

DatabaseDep = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    db: DatabaseDep, token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
        token_type = payload["type"]
        if token_type != "access":
            raise Exception
    except Exception:
        raise UnauthorizedError("Invalid or expired token")

    result = await db.scalars(select(User).where(User.id == user_id))
    user = result.one_or_none()

    if user is None:
        raise NotFoundError("User not found")
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def check_admin(user: CurrentUserDep):
    if not user.is_admin:
        raise PermissionDeniedError("Only admins can perform this action")


AdminDep = Annotated[None, Depends(check_admin)]


def get_job_filters(
    country: str | None = Query(default=None),
    company: str | None = Query(default=None),
    seniority: list[SeniorityLevel] = Query(default=[]),
    skills: list[str] = Query(default=[]),
    home_office: bool = Query(default=False),
) -> JobFilters:
    return JobFilters(
        country=country,
        company=company,
        seniority=seniority,
        skills=skills,
        with_home_office_only=home_office,
    )


JobFilterDep = Annotated[JobFilters, Depends(get_job_filters)]


async def get_username(form_data: OAuth2PasswordRequestForm = Depends()):
    return form_data.username
