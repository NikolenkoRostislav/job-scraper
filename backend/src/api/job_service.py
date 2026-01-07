from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import ARRAY, TEXT
from sqlalchemy import or_, select
from src.db.models import JobListing, Skill
from src.api.schemas import Filters


class JobService:
    @staticmethod
    async def get_jobs(page: int, page_size: int, filters: Filters, db: AsyncSession):
        stmt = select(JobListing)

        if filters.seniority:
            stmt = stmt.where(or_(
                JobListing.seniority_levels.cast(ARRAY(TEXT)).overlap(filters.seniority),
                JobListing.seniority_levels.is_(None)
            ))

        if filters.skills:
            stmt = stmt.join(JobListing.skills).where(Skill.name.in_(filters.skills)).distinct()

        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        
        result = await db.execute(stmt)
        jobs = result.scalars().all()
        return jobs

    @staticmethod
    async def get_job_by_id(job_id: int, db: AsyncSession):
        stmt = (
            select(JobListing)
            .where(JobListing.id == job_id)
        )

        result = await db.execute(stmt)
        job = result.scalar_one_or_none()
        return job

    @staticmethod
    async def get_job_skills(job_id: int, db: AsyncSession):
        stmt = (
            select(Skill)
            .join(JobListing.skills)
            .where(JobListing.id == job_id)
        )

        result = await db.execute(stmt)
        skills = result.scalars().all()
        return skills