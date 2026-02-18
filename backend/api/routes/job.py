from fastapi import APIRouter, Query

from api.dependencies import DatabaseDep, JobFilterDep
from shared.services import JobService
from shared.schemas import JobDetailed, JobListResponse, SkillBase
from shared.utils import JobOrder


PAGE_SIZE_DEFAULT = 20
PAGE_SIZE_MAX = 30
router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=JobListResponse)
async def get_jobs(
    db: DatabaseDep,
    order_by: JobOrder,
    filters: JobFilterDep,
    page: int = 1,
    page_size: int = Query(default=PAGE_SIZE_DEFAULT, le=PAGE_SIZE_MAX),
):
    return await JobService.get_jobs(db, page=page, page_size=page_size, order_by=order_by, filters=filters)


@router.get("/job-count", response_model=int)
async def get_job_count(db: DatabaseDep):
    return await JobService.get_job_count(db)


@router.get("/{job_id}/skills", response_model=list[SkillBase])
async def get_job_skills(db: DatabaseDep, job_id: int):
    return await JobService.get_job_skills(db, job_id)


@router.get("/{job_id}", response_model=JobDetailed | None)
async def get_job(db: DatabaseDep, job_id: int):
    return await JobService.get_job_by_id(db, job_id)
