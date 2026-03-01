from fastapi import APIRouter
from shared.schemas import JobFilters, UserBase, UserCreateWithEmail
from shared.services import EmailService, SavedFilterService, UserService
from shared.utils import PermissionDeniedError

from api.dependencies import CurrentUserDep, DatabaseDep, JobFilterDep
from api.exception_handler import responses_for

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/register",
    response_model=UserBase,
    status_code=201,
    responses=responses_for(400, 409),
)
async def register(db: DatabaseDep, user: UserCreateWithEmail, email_code: int):
    if not await EmailService.check_email_code(db, user.email, email_code):
        raise PermissionDeniedError("Incorrect code entered")
    return await UserService.create_user(db, user)


@router.get("/me", response_model=UserBase, responses=responses_for(401))
async def read_self(current_user: CurrentUserDep):
    return current_user


@router.get("/saved-filters", response_model=JobFilters, responses=responses_for(401))
async def get_filters(db: DatabaseDep, current_user: CurrentUserDep):
    return await SavedFilterService.get_filters(db, current_user.id)


@router.post("/save-filters", response_model=JobFilters, responses=responses_for(401))
async def save_filters(
    db: DatabaseDep, current_user: CurrentUserDep, filters: JobFilterDep
):
    return await SavedFilterService.save_filters(db, current_user.id, filters)
