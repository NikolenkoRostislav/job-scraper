from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from src.db.models import Skill, JobListingSkill
from src.utils.exceptions import *


class SkillService:
    @staticmethod
    async def get_top_skills(limit: int, db: AsyncSession):
        if limit <= 0:
            return {"skills": []}

        stmt = (
            select(Skill)
            .join(JobListingSkill)
            .group_by(Skill.id)
            .order_by(-func.count(JobListingSkill.job_listing_id))
            .limit(limit)
        )

        result = await db.execute(stmt)
        skills = result.scalars().all()
        return {"skills": skills}

    @staticmethod
    async def get_skill_by_name(skill_name: str, db: AsyncSession):
        stmt = (
            select(Skill, func.count(JobListingSkill.job_listing_id).label("job_count"))
            .join(JobListingSkill)
            .where(Skill.name == skill_name)
            .group_by(Skill.id)
        )

        result = await db.execute(stmt)
        row = result.first()
        if row:
            skill, job_count = row
            return {"skill": skill, "job_count": job_count}
        raise NotFoundError("Skill not found")

    @staticmethod
    async def create_skill(canonical_name, category, db: AsyncSession):
        result = await db.execute(select(Skill).where(Skill.name == canonical_name))
        skill = result.scalar_one_or_none()

        if not skill:
            skill = Skill(name=canonical_name, category=category)
            db.add(skill)
            await db.commit()

        return skill

    @staticmethod
    async def link_skill_to_job(job_id, skill_id, db: AsyncSession):
        result = await db.execute(
            select(JobListingSkill).where(
                JobListingSkill.job_listing_id == job_id,
                JobListingSkill.skill_id == skill_id,
            )
        )
        link = result.scalar_one_or_none()
        
        if not link:
            link = JobListingSkill(job_listing_id=job_id, skill_id=skill_id)
            db.add(link)
            await db.commit()

        return link
