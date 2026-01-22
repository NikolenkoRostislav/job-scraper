from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator
from src.utils.parsers import parse_seniority_list, parse_skill_list, parse_country
from src.utils.normalizer import normalize_string
from src.utils.enums import SeniorityLevel
from src.utils.security import validate_password_complexity


class Filters(BaseModel):
    seniority: list[SeniorityLevel]
    skills: list[str]
    country: str | None = None
    company: str | None = None

    @field_validator("seniority", mode="before")
    @classmethod
    def validate_seniority(cls, v):
        seniority_list = parse_seniority_list(v or [])
        return [s for s in seniority_list if s is not None]

    @field_validator("skills", mode="before")
    @classmethod
    def validate_skills(cls, v):
        skill_list = parse_skill_list(v or [], strict=True)
        return [skill for skill, category in skill_list if skill is not None]

    @field_validator("country", mode="before")
    @classmethod
    def validate_country(cls, v):
        return parse_country(v)

    @field_validator("company", mode="before")
    @classmethod
    def normalize_company(cls, v):
        return normalize_string(v)


class SkillBase(BaseModel):
    id: int
    name: str
    category: str | None = None

    class Config:
        from_attributes = True


class JobBase(BaseModel):
    id: int
    url: str
    title: str
    location: str | None = None
    country: str | None = None
    company: str | None = None
    seniority_levels: list[str] | None = None
    home_office: bool | None = None
    created_at: datetime | None = None
    last_updated_at: datetime | None = None
    last_seen_at: datetime | None = None

    class Config:
        from_attributes = True


class JobDetailed(JobBase):
    description: str | None = None
    source_website: str | None = None


class JobListResponse(BaseModel):
    jobs: list[JobBase]
    size: int


class SkillListResponse(BaseModel):
    skills: list[SkillBase]


class SkillDetailResponse(BaseModel):
    skill: SkillBase
    job_count: int


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

class Token(BaseModel):
    access_token: str
    token_type: str

class Tokens(Token):
    refresh_token: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str
