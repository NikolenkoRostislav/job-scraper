from fastapi import APIRouter
from src.services import UserService, JobService, SavedFilterService, EmailService
from src.schemas import UserCreateWithEmail, UserBase, JobListResponse, JobFilters
from src.api.dependencies import DatabaseDep, CurrentUserDep
from src.api.exception_handler import handle_exceptions
from src.utils.classes import PermissionDeniedError


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=UserBase)
@handle_exceptions
async def register(user: UserCreateWithEmail, email_code: int, db: DatabaseDep):
    if not await EmailService.check_email_code(user.email, email_code, db):
        raise PermissionDeniedError("Incorrect code entered")
    return await UserService.create_user(user, db)


@router.get("/me", response_model=UserBase)
@handle_exceptions
async def read_self(current_user: CurrentUserDep):
    return current_user


@router.get("/favorited-jobs", response_model=JobListResponse)
@handle_exceptions
async def get_favorited_jobs(current_user: CurrentUserDep, db: DatabaseDep):
    return await JobService.get_favorited_jobs(current_user.id, db)


@router.get("/saved-filters", response_model=JobFilters)
@handle_exceptions
async def get_filters(current_user: CurrentUserDep, db: DatabaseDep):
    return await SavedFilterService.get_filters(current_user.id, db)