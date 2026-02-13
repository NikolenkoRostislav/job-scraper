from fastapi import APIRouter

from api.dependencies import DatabaseDep, CurrentUserDep, JobFilterDep
from shared.services import FavoriteJobService
from shared.schemas import JobDetailed, JobListResponse


router = APIRouter(prefix="/favorited-jobs", tags=["favorited-jobs"])


@router.get("/", response_model=JobListResponse)
async def get_favorited_jobs(db: DatabaseDep, current_user: CurrentUserDep, filters: JobFilterDep):
    return await FavoriteJobService.get_favorited_jobs(db, current_user.id, filters=filters)


@router.get("/{job_id}/is-favorited", response_model=bool)
async def check_job_favorited(db: DatabaseDep, current_user: CurrentUserDep, job_id: int):
    return await FavoriteJobService.check_job_favorited(db, current_user.id, job_id)


@router.post("/{job_id}/favorite", response_model=JobDetailed)
async def favorite_job(db: DatabaseDep, user: CurrentUserDep, job_id: int):
    return await FavoriteJobService.favorite_job(db, user.id, job_id)


@router.delete("/{job_id}/unfavorite")
async def unfavorite_job(db: DatabaseDep, user: CurrentUserDep, job_id: int):
    return await FavoriteJobService.unfavorite_job(db, user.id, job_id)
