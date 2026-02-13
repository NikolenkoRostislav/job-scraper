from fastapi import APIRouter

from shared.services import UserService, JobService, SavedFilterService, EmailService
from shared.schemas import UserCreateWithEmail, UserBase, JobListResponse, JobFilters
from shared.utils import PermissionDeniedError
from api.dependencies import DatabaseDep, CurrentUserDep, JobFilterDep


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=UserBase)
async def register(db: DatabaseDep, user: UserCreateWithEmail, email_code: int):
    if not await EmailService.check_email_code(db, user.email, email_code):
        raise PermissionDeniedError("Incorrect code entered")
    return await UserService.create_user(db, user)


@router.get("/me", response_model=UserBase)
async def read_self(current_user: CurrentUserDep):
    return current_user


@router.get("/saved-filters", response_model=JobFilters)
async def get_filters(db: DatabaseDep, current_user: CurrentUserDep):
    return await SavedFilterService.get_filters(db, current_user.id)