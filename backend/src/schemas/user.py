from pydantic import BaseModel, EmailStr, field_validator
from src.utils.security import validate_password_complexity


class UserBase(BaseModel):
    id: int
    username: str


class UserCreate(BaseModel):
    """ SHOULD NEVER BE RETURNED!!! """
    email: EmailStr
    username: str
    password: str 

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password_complexity(v)
