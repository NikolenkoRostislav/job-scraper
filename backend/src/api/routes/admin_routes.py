from fastapi import APIRouter
from src.api.dependencies import DatabaseDep, AdminDep
from src.api.exception_handler import handle_exceptions
from src.services import JobService


router = APIRouter(prefix="/admin", tags=["admin"])


@router.delete("/job/{job_id}")
@handle_exceptions
async def delete_job(db: DatabaseDep, admin: AdminDep, job_id: int):
    return await JobService.delete_job(job_id, db)
