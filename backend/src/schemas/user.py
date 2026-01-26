from pydantic import BaseModel, EmailStr, field_validator, model_validator
from src.utils.security import validate_password_complexity


class UserBase(BaseModel):
    id: int
    username: str


class UserCreate(BaseModel):
    """ SHOULD NEVER BE RETURNED!!! """
    email: EmailStr
    username: str
    password: str | None = None
    google_id: str | None = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str | None) -> str | None:
        return validate_password_complexity(v)
    
    @model_validator(mode="before")
    @classmethod
    def check_password_or_google_id(cls, values):
        password = values.get("password")
        google_id = values.get("google_id")

        if (password is None and google_id is None) or (password is not None and google_id is not None):
            raise ValueError("Either password or google_id must be provided, but not both or neither")
        return values
