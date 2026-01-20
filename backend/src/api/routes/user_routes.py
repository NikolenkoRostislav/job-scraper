from fastapi import APIRouter
from src.api.schemas import UserCreate, UserBase, JobListResponse
from src.services import UserService, JobService
from src.api.dependancies import DatabaseDep, CurrentUserDep
from src.api.exception_handler import handle_exceptions


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=UserBase)
@handle_exceptions
async def register(user: UserCreate, db: DatabaseDep):
    return await UserService.create_user(user, db)


@router.get("/me", response_model=UserBase)
@handle_exceptions
async def read_self(current_user: CurrentUserDep):
    return current_user


@router.get("/favorited-jobs", response_model=JobListResponse)
@handle_exceptions
async def get_favorited_jobs(current_user: CurrentUserDep, db: DatabaseDep):
    return await JobService.get_favorited_jobs(current_user.id, db)
