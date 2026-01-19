from fastapi import APIRouter, Query
from src.services import JobService
from src.api.schemas import Filters
from src.db.session import DatabaseDep
from src.api.schemas import JobDetailed, JobListResponse, SkillListResponse
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
    filters = Filters(
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