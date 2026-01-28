from pydantic import BaseModel, EmailStr, field_validator
from src.utils.security import validate_password_complexity


class UserBase(BaseModel):
    id: int
    username: str


class UserCreateBase(BaseModel):
    email: EmailStr
    username: str

class UserCreateWithEmail(UserCreateBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str | None) -> str | None:
        return validate_password_complexity(v)

class UserCreateWithGmail(UserCreateBase):
    google_id: str
