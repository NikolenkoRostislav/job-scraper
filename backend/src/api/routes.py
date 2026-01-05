from fastapi import APIRouter
from src.api.job_service import JobService
from src.api.skill_service import SkillService
from src.api.filters_parser import parse_filters
from src.db.session import DatabaseDep


router = APIRouter()

@router.get("/jobs")
async def get_jobs(db: DatabaseDep, page: int, page_size: int, filters: str | None = None):
    normalized_filters = parse_filters(filters)
    return await JobService.get_jobs(page, page_size, normalized_filters, db)

@router.get("/jobs/{job_id}/skills")
async def get_job_skills(db: DatabaseDep, job_id: int):
    return await JobService.get_job_skills(job_id, db)

@router.get("/jobs/{job_id}")
async def get_job(db: DatabaseDep, job_id: int):
    return await JobService.get_job_by_id(job_id, db)

@router.get("/skills/ranking/{limit}")
async def get_skills(db: DatabaseDep, limit: int):
    return await SkillService.get_top_skills(limit, db)

@router.get("/skills/{skill_name}")
async def get_skill(db: DatabaseDep, skill_name: str):
    return await SkillService.get_skill_by_name(skill_name, db)