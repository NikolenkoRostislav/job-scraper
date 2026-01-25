from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, or_, select, func
from src.db.models import JobListing, Skill, FavoritedJobListing
from src.schemas import JobFilters, JobCreate, DateRange
from src.utils.classes import NotFoundError, AlreadyExistsError


class JobService:
    @staticmethod
    async def get_jobs(page: int, page_size: int, filters: JobFilters, db: AsyncSession):
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
    async def create_or_update_job(job_data: JobCreate, db: AsyncSession):
        changed = False

        result = await db.scalars(
            select(JobListing).where(JobListing.url == job_data.url)
        )
        job = result.one_or_none()

        if job:
            fields = {
                "title": job_data.title,
                "description": job_data.description,
                "location": job_data.location,
                "country": job_data.country,
                "home_office": job_data.home_office,
            }

            for field, new_value in fields.items():
                if getattr(job, field) != new_value:
                    setattr(job, field, new_value)
                    changed = True

            if set(job.seniority_levels) != set(job_data.seniority_levels):
                job.seniority_levels = job_data.seniority_levels
                changed = True

            if changed:
                job.last_updated_at = datetime.now(timezone.utc)
            job.last_seen_at = datetime.now(timezone.utc)
        else:
            job = JobListing(
                url=job_data.url,
                title=job_data.title,
                description=job_data.description,
                location=job_data.location,
                country=job_data.country,
                company=job_data.company,
                source_website=job_data.source_website,
                home_office=job_data.home_office,
                seniority_levels=job_data.seniority_levels,
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
    

    @staticmethod
    async def delete_job(job_id: int, db: AsyncSession):
        result = await db.scalars(select(JobListing).where(JobListing.id == job_id))
        job = result.one_or_none()

        if not job:
            raise NotFoundError(f"Job with id {job_id} not found")

        await db.delete(job)
        await db.commit()
        return {"message": f"Job with id {job_id} deleted"}


    @staticmethod
    async def get_job_count(date_range: DateRange, db: AsyncSession) -> int:
        stmt = select(func.count(JobListing.id))
        
        conditions = []
        
        if date_range.start_time:
            conditions.append(JobListing.created_at >= date_range.start_time)
        
        if date_range.end_time:
            conditions.append(JobListing.created_at <= date_range.end_time)
        
        if conditions:
            stmt = stmt.where(and_(*conditions))
        
        result = await db.scalar(stmt)
        return result or 0


    @staticmethod
    async def get_outdated_jobs(cutoff_time: datetime, db: AsyncSession):
        stmt = select(JobListing).where(JobListing.last_seen_at < cutoff_time)
        
        result = await db.scalars(stmt)
        jobs = result.all()
        
        return {"jobs": jobs, "size": len(jobs)}
