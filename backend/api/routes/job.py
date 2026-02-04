from fastapi import APIRouter, Query

from api.dependencies import DatabaseDep, CurrentUserDep, JobFilterDep
from shared.services import JobService, SavedFilterService
from shared.schemas import JobFilters, JobDetailed, JobListResponse, SkillBase
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


@router.post("/save-filters", response_model=JobFilters)
async def save_filters(db: DatabaseDep, current_user: CurrentUserDep, filters: JobFilterDep):
    return await SavedFilterService.save_filters(db, current_user.id, filters)


@router.post("/{job_id}/favorite", response_model=JobDetailed)
async def favorite_job(db: DatabaseDep, user: CurrentUserDep, job_id: int):
    return await JobService.favorite_job(db, user.id, job_id)


@router.delete("/{job_id}/unfavorite")
async def unfavorite_job(db: DatabaseDep, user: CurrentUserDep, job_id: int):
    return await JobService.unfavorite_job(db, user.id, job_id)
