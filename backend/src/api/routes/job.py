from fastapi import APIRouter, Query
from src.services import JobService
from src.schemas import JobFilters, JobDetailed, JobListResponse, SkillListResponse
from src.api.dependencies import DatabaseDep, CurrentUserDep
from src.api.exception_handler import handle_exceptions


PAGE_SIZE_DEFAULT = 20
PAGE_SIZE_MAX = 30
router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=JobListResponse)
@handle_exceptions
async def get_jobs(
    db: DatabaseDep,
    page: int = 1,
    page_size: int = Query(default=PAGE_SIZE_DEFAULT, le=PAGE_SIZE_MAX),
    country: str | None = Query(default=None),
    company: str | None = Query(default=None),
    seniority: list[str] = Query(default=[]),
    skills: list[str] = Query(default=[]),
):
    filters = JobFilters(
        seniority=seniority, company=company, skills=skills, country=country
    )
    return await JobService.get_jobs(page, page_size, filters, db)


@router.get("/{job_id}/skills", response_model=SkillListResponse)
@handle_exceptions
async def get_job_skills(db: DatabaseDep, job_id: int):
    return await JobService.get_job_skills(job_id, db)


@router.get("/{job_id}", response_model=JobDetailed | None)
@handle_exceptions
async def get_job(db: DatabaseDep, job_id: int):
    return await JobService.get_job_by_id(job_id, db)


@router.post("/{job_id}/favorite", response_model=JobDetailed)
@handle_exceptions
async def favorite_job(db: DatabaseDep, user: CurrentUserDep, job_id: int):
    return await JobService.favorite_job(job_id, user.id, db)


@router.delete("/{job_id}/unfavorite")
@handle_exceptions
async def unfavorite_job(db: DatabaseDep, user: CurrentUserDep, job_id: int):
    return await JobService.unfavorite_job(job_id, user.id, db)


@router.post("/save-filters", response_model=JobFilters)
@handle_exceptions
async def save_filters(current_user: CurrentUserDep, db: DatabaseDep, filters: JobFilters):
    return await JobService.save_filters(filters, current_user.id, db)
