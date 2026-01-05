from sqlalchemy.ext.asyncio import AsyncSession


class JobService:
    @staticmethod
    async def get_jobs(page: int, page_size: int, filters: dict, db: AsyncSession):
        pass

    @staticmethod
    async def get_job_by_id(job_id: int, db: AsyncSession):
        pass

    @staticmethod
    async def get_job_skills(job_id: int, db: AsyncSession):
        pass
