from fastapi import APIRouter

from src.services import UserService, JobService, SavedFilterService, EmailService
from src.schemas import UserCreateWithEmail, UserBase, JobListResponse, JobFilters
from src.api.dependencies import DatabaseDep, CurrentUserDep, JobFilterDep
from src.utils import PermissionDeniedError


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=UserBase)
async def register(db: DatabaseDep, user: UserCreateWithEmail, email_code: int):
    if not await EmailService.check_email_code(db, user.email, email_code):
        raise PermissionDeniedError("Incorrect code entered")
    return await UserService.create_user(db, user)


@router.get("/me", response_model=UserBase)
async def read_self(current_user: CurrentUserDep):
    return current_user


@router.get("/favorited-jobs", response_model=JobListResponse)
async def get_favorited_jobs(db: DatabaseDep, current_user: CurrentUserDep, filters: JobFilterDep):
    return await JobService.get_favorited_jobs(db, current_user.id, filters=filters)


@router.get("/saved-filters", response_model=JobFilters)
async def get_filters(db: DatabaseDep, current_user: CurrentUserDep):
    return await SavedFilterService.get_filters(db, current_user.id)