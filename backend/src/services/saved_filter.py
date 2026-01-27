from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Skill, SavedFilter
from src.utils.classes import NotFoundError
from src.schemas import JobFilters


class SavedFilterService:
    @staticmethod
    async def get_filters(user_id: int, db: AsyncSession) -> JobFilters:
        result = await db.scalars(
            select(SavedFilter)
            .options(selectinload(SavedFilter.skills))
            .where(SavedFilter.user_id == user_id)
        )
        saved_filter = result.one_or_none()

        if not saved_filter:
            raise NotFoundError("Saved filters not found")

        return JobFilters(
            seniority=saved_filter.seniority or [],
            skills=[skill.name for skill in saved_filter.skills],
            country=saved_filter.country,
            company=saved_filter.company,
            with_home_office_only=saved_filter.with_home_office_only
        )
    

    @staticmethod
    async def save_filters(filters: JobFilters, user_id: int, db: AsyncSession) -> JobFilters:
        result = await db.scalars(
            select(SavedFilter)
            .options(selectinload(SavedFilter.skills))
            .where(SavedFilter.user_id == user_id)
        )
        saved_filter = result.one_or_none()

        skills_result = await db.scalars(
            select(Skill)
            .where(Skill.name.in_(filters.skills))
        )
        skills = list(skills_result)

        if saved_filter:
            saved_filter.seniority = filters.seniority
            saved_filter.country = filters.country
            saved_filter.company = filters.company
            saved_filter.skills = skills
            saved_filter.with_home_office_only = filters.with_home_office_only
        else:
            saved_filter = SavedFilter(
                user_id=user_id,
                seniority=filters.seniority,
                country=filters.country,
                company=filters.company,
                skills=skills,
                with_home_office_only = filters.with_home_office_only
            )
            db.add(saved_filter)

        await db.commit()
        return filters
