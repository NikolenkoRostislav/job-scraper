from datetime import datetime, timezone

from sqlalchemy import and_, or_, select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import JobListing, Skill, FavoritedJobListing
from src.schemas import JobFilters, JobCreate, DateRange, JobDetailed
from src.utils import NotFoundError, AlreadyExistsError, JobOrder


def _add_filter_conditions(stmt, filters: JobFilters):
        conditions = []

        if filters.seniority:
            conditions.append(
                JobListing.seniority_levels.overlap(filters.seniority)
            )

        if filters.skills:
            stmt = stmt.join(JobListing.skills)
            conditions.append(
                Skill.name.in_(filters.skills)
            )

        if filters.country:
            conditions.append(
                or_(
                    JobListing.country == filters.country,
                    JobListing.country.is_(None),
                )
            )

        if filters.company:
            conditions.append(
                func.trim(func.lower(JobListing.company)) == filters.company
            )

        if filters.with_home_office_only:
            conditions.append(
                JobListing.home_office.is_(True)
            )

        if conditions:
            stmt = stmt.where(and_(*conditions))

        return stmt


class JobService:
    @staticmethod
    async def get_jobs(db: AsyncSession, page: int, page_size: int, order_by: JobOrder, filters: JobFilters):
        if page <= 0 or page_size <= 0:
            return {"jobs": [], "size": 0}

        stmt = select(JobListing)
        stmt = _add_filter_conditions(stmt, filters)
        
        if order_by.value == "favorites": 
            stmt = stmt.outerjoin(
                FavoritedJobListing,
                FavoritedJobListing.job_listing_id == JobListing.id
            ).group_by(JobListing.id).order_by(
                desc(func.count(FavoritedJobListing.job_listing_id))
            )
        elif order_by.value == "update_time":
            stmt = stmt.order_by(desc(JobListing.last_updated_at))
        elif order_by.value == "creation_time":
            stmt = stmt.order_by(desc(JobListing.created_at))

        stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        result = await db.scalars(stmt)
        jobs = result.all()

        return {"jobs": jobs}


    @staticmethod
    async def get_job_by_id(db: AsyncSession, job_id: int):
        stmt = (
            select(JobListing)
            .where(JobListing.id == job_id)
            .options(selectinload(JobListing.skills))
        )

        result = await db.scalars(stmt)
        job = result.one_or_none()
        if not job:
            raise NotFoundError("Job not found")
        return job


    @staticmethod
    async def get_job_skills(db: AsyncSession, job_id: int):
        job = await JobService.get_job_by_id(db, job_id) 
        return job.skills
    

    @staticmethod
    async def create_or_update_job(db: AsyncSession, job_data: JobCreate):
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
    async def favorite_job(db: AsyncSession, user_id: int, job_id: int):
        job = await JobService.get_job_by_id(db, job_id) # raises exception if job doesnt exist

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
    async def unfavorite_job(db: AsyncSession, user_id: int, job_id: int):
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
    async def get_favorited_jobs(db: AsyncSession, user_id: int, filters: JobFilters):
        stmt = select(JobListing).join(FavoritedJobListing).where(FavoritedJobListing.user_id == user_id)
        stmt = _add_filter_conditions(stmt, filters)

        result = await db.scalars(stmt)
        jobs = result.all()
        return {"jobs": jobs}
    

    @staticmethod
    async def delete_job(db: AsyncSession, job_id: int):
        result = await db.scalars(select(JobListing).where(JobListing.id == job_id))
        job = result.one_or_none()

        if not job:
            raise NotFoundError(f"Job with id {job_id} not found")

        await db.delete(job)
        await db.commit()
        return {"message": f"Job with id {job_id} deleted"}


    @staticmethod
    async def get_job_count(db: AsyncSession, date_range: DateRange | None = None) -> int:
        stmt = select(func.count(JobListing.id))
        
        if date_range:
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
    async def get_outdated_jobs(db: AsyncSession, cutoff_time: datetime):
        stmt = select(JobListing).where(JobListing.last_seen_at < cutoff_time)
        
        result = await db.scalars(stmt)
        jobs = result.all()
        
        return {"jobs": jobs}
