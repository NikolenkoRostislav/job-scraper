from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select, func
from src.utils.parsers import parse_seniority_list
from src.db.models import JobListing, Skill, FavoritedJobListing
from src.api.schemas import Filters
from src.utils.exceptions import *


class JobService:
    @staticmethod
    async def get_jobs(page: int, page_size: int, filters: Filters, db: AsyncSession):
        if page <= 0 or page_size <= 0:
            return {"jobs": [], "size": 0}

        stmt = select(JobListing)

        if filters.seniority:
            stmt = stmt.where(
                JobListing.seniority_levels.overlap(
                    filters.seniority
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

        result = await db.scalars(stmt)
        jobs = result.all()
        return {"jobs": jobs, "size": len(jobs)}

    @staticmethod
    async def get_job_by_id(job_id: int, db: AsyncSession):
        stmt = select(JobListing).where(JobListing.id == job_id)

        result = await db.scalars(stmt)
        job = result.one_or_none()
        if not job:
            raise NotFoundError("Job not found")
        return job

    @staticmethod
    async def get_job_skills(job_id: int, db: AsyncSession):
        job = await JobService.get_job_by_id(job_id, db) # raise exception if job doesnt exist
 
        stmt = select(Skill).join(JobListing.skills).where(JobListing.id == job_id)

        result = await db.scalars(stmt)
        skills = result.all()
        return {"skills": skills}
    
    @staticmethod
    async def create_or_update_job(job_data, db: AsyncSession): # job_data can be a scrapy item adapter or a dict
        changed = False
        seniority_list = parse_seniority_list(job_data.get("seniority_levels", []))

        result = await db.scalars(
            select(JobListing).where(JobListing.url == job_data.get("url"))
        )
        job = result.one_or_none()

        if job:
            fields = {  # I'll add support for checking seniority list changes later but it's always updated for now
                "title": job_data.get("title"),
                "description": job_data.get("description"),
                "location": job_data.get("location"),
                "country": job_data.get("country"),
                "home_office": job_data.get("home_office"),
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
                url=job_data.get("url"),
                title=job_data.get("title"),
                description=job_data.get("description"),
                location=job_data.get("location"),
                country=job_data.get("country"),
                company=job_data.get("company"),
                source_website=job_data.get("source_website"),
                home_office=job_data.get("home_office"),
                seniority_levels=seniority_list,
                created_at=datetime.now(timezone.utc),
                last_updated_at=datetime.now(timezone.utc),
                last_seen_at=datetime.now(timezone.utc),
            )
            db.add(job)
        await db.commit()
        return {"job": job, "changed": changed}
    

    @staticmethod
    async def favorite_job(job_id: int, user_id: int, db: AsyncSession):
        job = await JobService.get_job_by_id(job_id, db) # raise exception if job doesnt exist

        try:
            favorited_job = FavoritedJobListing(
                user_id=user_id,
                job_listing_id=job_id
            ) 
            db.add(favorited_job)
            await db.commit()
        except Exception:
            raise AlreadyExistsError("Job already favorited")
        return job
    

    @staticmethod
    async def unfavorite_job(job_id: int, user_id: int, db: AsyncSession):
        result = await db.scalars(
            select(FavoritedJobListing)
            .where((FavoritedJobListing.user_id == user_id) & (FavoritedJobListing.job_listing_id == job_id))
        )

        favorited_job = result.one_or_none()
        if not favorited_job:
            return {"message": "Favorited job not found"}
        
        await db.delete(favorited_job)
        await db.commit()
        return {"message": "Job unfavorited"}


    @staticmethod
    async def get_favorited_jobs(user_id: int, db: AsyncSession):
        result = await db.scalars(
            select(JobListing).join(FavoritedJobListing).where(FavoritedJobListing.user_id == user_id)
        )
        jobs = result.all()
        return {"jobs": jobs, "size": len(jobs)}
