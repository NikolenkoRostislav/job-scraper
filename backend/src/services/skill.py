from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, desc

from src.models import Skill, JobListingSkill
from src.utils import NotFoundError
from src.services.job import JobService


class SkillService:
    @staticmethod
    async def get_top_skills(db: AsyncSession, limit: int):
        if limit <= 0:
            return {"skills": []}

        stmt = (
            select(Skill, func.count(JobListingSkill.job_listing_id).label("job_count"))
            .join(JobListingSkill)
            .group_by(Skill.id)
            .order_by(desc(func.count(JobListingSkill.job_listing_id)))
            .limit(limit)
        )

        result = await db.execute(stmt)
        rows = result.all()

        total_job_count = await JobService.get_job_count(db)

        return {
            "skills": [
                {
                    "skill": skill,
                    "job_count": job_count,
                    "frequency": job_count / total_job_count 
                }
                for skill, job_count in rows
            ]
        }


    @staticmethod
    async def get_skill_by_name(db: AsyncSession, skill_name: str):
        stmt = (
            select(Skill, func.count(JobListingSkill.job_listing_id).label("job_count"))
            .join(JobListingSkill)
            .where(Skill.name == skill_name)
            .group_by(Skill.id)
        )

        result = await db.execute(stmt)
        row = result.first()

        total_job_count = await JobService.get_job_count(db)

        if row:
            skill, job_count = row
            return {"skill": skill, "job_count": job_count, "frequency": job_count / total_job_count}
        raise NotFoundError("Skill not found")


    @staticmethod
    async def create_skill(db: AsyncSession, canonical_name: str, category: str):
        result = await db.scalars(select(Skill).where(Skill.name == canonical_name))
        skill = result.one_or_none()

        if not skill:
            skill = Skill(name=canonical_name, category=category)
            db.add(skill)
            await db.commit()

        return skill


    @staticmethod
    async def link_skill_to_job(db: AsyncSession, job_id: int, skill_id: int):
        result = await db.scalars(
            select(JobListingSkill).where(
                JobListingSkill.job_listing_id == job_id,
                JobListingSkill.skill_id == skill_id,
            )
        )
        link = result.one_or_none()
        
        if not link:
            link = JobListingSkill(job_listing_id=job_id, skill_id=skill_id)
            db.add(link)
            await db.commit()

        return link
