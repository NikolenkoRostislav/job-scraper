from fastapi import APIRouter
from shared.schemas import JobDetailed, JobListResponse
from shared.services import FavoriteJobService

from api.dependencies import CurrentUserDep, DatabaseDep, JobFilterDep
from api.exception_handler import responses_for

router = APIRouter(prefix="/favorited-jobs", tags=["favorited-jobs"])


@router.get("/", response_model=JobListResponse, responses=responses_for(401))
async def get_favorited_jobs(
    db: DatabaseDep, current_user: CurrentUserDep, filters: JobFilterDep
):
    return await FavoriteJobService.get_favorited_jobs(
        db, current_user.id, filters=filters
    )


@router.get("/{job_id}/is-favorited", response_model=bool, responses=responses_for(401))
async def check_job_favorited(
    db: DatabaseDep, current_user: CurrentUserDep, job_id: int
):
    return await FavoriteJobService.check_job_favorited(db, current_user.id, job_id)


@router.post(
    "/{job_id}/favorite",
    response_model=JobDetailed,
    responses=responses_for(401, 404, 409),
)
async def favorite_job(db: DatabaseDep, user: CurrentUserDep, job_id: int):
    return await FavoriteJobService.favorite_job(db, user.id, job_id)


@router.delete("/{job_id}/unfavorite", responses=responses_for(401))
async def unfavorite_job(db: DatabaseDep, user: CurrentUserDep, job_id: int):
    return await FavoriteJobService.unfavorite_job(db, user.id, job_id)
