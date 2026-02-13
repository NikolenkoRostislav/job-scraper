from datetime import datetime, timezone

from sqlalchemy import and_, or_, select, desc, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shared.services.job import JobService
from shared.models import JobListing, FavoritedJobListing
from shared.schemas import JobFilters
from shared.utils import AlreadyExistsError


class FavoriteJobService:
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
        stmt = JobService.add_filter_conditions(stmt, filters)

        result = await db.scalars(stmt)
        jobs = result.all()
        return {"jobs": jobs}
    

    @staticmethod 
    async def check_job_favorited(db: AsyncSession, user_id: int, job_id: int):
        stmt = (
            select(JobListing)
            .join(FavoritedJobListing)
            .where(and_(
                FavoritedJobListing.user_id == user_id, 
                FavoritedJobListing.job_listing_id == job_id
            ))
        )
        
        result = await db.scalars(stmt)
        job = result.one_or_none()
        return bool(job)
