from fastapi import APIRouter
from src.api.schemas import UserCreate, UserBase
from src.api.user_service import UserService
from src.db.session import DatabaseDep
from src.api.auth_service import CurrentUserDep


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=UserBase)
async def register(user: UserCreate, db: DatabaseDep):
    return await UserService.create_user(user, db)


@router.get("/me", response_model=UserBase)
async def read_self(current_user: CurrentUserDep):
    return current_user