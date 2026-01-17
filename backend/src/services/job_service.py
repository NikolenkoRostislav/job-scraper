from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import ARRAY, TEXT
from sqlalchemy import or_, select, func
from src.utils.parsers import parse_seniority_list
from src.db.models import JobListing, Skill
from src.api.schemas import Filters


class JobService:
    @staticmethod
    async def get_jobs(page: int, page_size: int, filters: Filters, db: AsyncSession):
        if page <= 0 or page_size <= 0:
            return {"jobs": [], "size": 0}

        stmt = select(JobListing)

        if filters.seniority:
            stmt = stmt.where(
                or_(
                    JobListing.seniority_levels.cast(ARRAY(TEXT)).overlap(
                        filters.seniority
                    ),
                    JobListing.seniority_levels.is_(None),
                )
            )

        if filters.skills:
            stmt = (
                stmt.join(JobListing.skills)
                .where(Skill.name.in_(filters.skills))
                .distinct()
            )

        if filters.country:
            stmt = stmt.where(
                or_(JobListing.country == filters.country, JobListing.country.is_(None))
            )

        if filters.company:
            stmt = stmt.where(
                func.trim(func.lower(JobListing.company)) == filters.company,
            )

        stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        result = await db.execute(stmt)
        jobs = result.scalars().all()
        return {"jobs": jobs, "size": len(jobs)}

    @staticmethod
    async def get_job_by_id(job_id: int, db: AsyncSession):
        stmt = select(JobListing).where(JobListing.id == job_id)

        result = await db.execute(stmt)
        job = result.scalar_one_or_none()
        return job

    @staticmethod
    async def get_job_skills(job_id: int, db: AsyncSession):
        stmt = select(Skill).join(JobListing.skills).where(JobListing.id == job_id)

        result = await db.execute(stmt)
        skills = result.scalars().all()
        return {"skills": skills}
    
    @staticmethod
    async def create_or_update_job(adapter, db: AsyncSession): # adapter is a scrapy item adapter, I'll change this later
        changed = False
        seniority_list = parse_seniority_list(adapter.get("seniority_levels", []))

        result = await db.execute(
            select(JobListing).where(JobListing.url == adapter.get("url"))
        )
        job = result.scalar_one_or_none()

        if job:
            fields = {  # I'll add support for checking seniority list changes later but it's always updated for now
                "title": adapter.get("title"),
                "description": adapter.get("description"),
                "location": adapter.get("location"),
                "country": adapter.get("country"),
                "home_office": adapter.get("home_office"),
            }

            for field, new_value in fields.items():
                if getattr(job, field) != new_value:
                    setattr(job, field, new_value)
                    changed = True

            if changed:
                setattr(job, "last_updated_at", datetime.now(timezone.utc))
            setattr(job, "seniority_levels", seniority_list)
            setattr(job, "last_seen_at", datetime.now(timezone.utc))
        else:
            job = JobListing(
                url=adapter.get("url"),
                title=adapter.get("title"),
                description=adapter.get("description"),
                location=adapter.get("location"),
                country=adapter.get("country"),
                company=adapter.get("company"),
                source_website=adapter.get("source_website"),
                home_office=adapter.get("home_office"),
                seniority_levels=seniority_list,
                created_at=datetime.now(timezone.utc),
                last_updated_at=datetime.now(timezone.utc),
                last_seen_at=datetime.now(timezone.utc),
            )
            db.add(job)
        await db.commit()
        return {"job": job, "changed": changed}

