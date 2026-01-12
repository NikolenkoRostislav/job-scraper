from fastapi import APIRouter, Query, Path
from src.api.job_service import JobService
from src.api.skill_service import SkillService
from src.api.schemas import Filters
from src.db.session import DatabaseDep
from src.api.schemas import JobBase, JobListResponse, SkillListResponse, SkillDetailResponse


PAGE_SIZE_DEFAULT = 20
PAGE_SIZE_MAX = 30
SKILL_RANKING_MAX = 50

router = APIRouter()

@router.get("/jobs", response_model=JobListResponse)
async def get_jobs(db: DatabaseDep, page: int = 1, 
    page_size: int = Query(default=PAGE_SIZE_DEFAULT, le=PAGE_SIZE_MAX),
    country: str | None = Query(default=None),
    seniority: list[str] = Query(default=[]),
    skills: list[str] = Query(default=[])
):
    filters = Filters(seniority=seniority, skills=skills, country=country)
    return await JobService.get_jobs(page, page_size, filters, db)

@router.get("/jobs/{job_id}/skills", response_model=SkillListResponse)
async def get_job_skills(db: DatabaseDep, job_id: int):
    return await JobService.get_job_skills(job_id, db)

@router.get("/jobs/{job_id}", response_model=JobBase | None)
async def get_job(db: DatabaseDep, job_id: int):
    return await JobService.get_job_by_id(job_id, db)

@router.get("/skills/ranking/{limit}", response_model=SkillListResponse)
async def get_skills(db: DatabaseDep, limit: int = Path(le=SKILL_RANKING_MAX)):
    return await SkillService.get_top_skills(limit, db)

@router.get("/skills/{skill_name}", response_model=SkillDetailResponse | None)
async def get_skill(db: DatabaseDep, skill_name: str):
    return await SkillService.get_skill_by_name(skill_name, db)
