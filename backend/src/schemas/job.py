from datetime import datetime
from pydantic import BaseModel, field_validator
from src.utils.parsers import parse_seniority_list, parse_skill_list, parse_country
from src.utils.normalizer import normalize_string
from src.utils.classes.enums import SeniorityLevel


class JobFilters(BaseModel):
    seniority: list[SeniorityLevel]
    skills: list[str]
    country: str | None = None
    company: str | None = None
    with_home_office_only: bool = False

    @field_validator("seniority", mode="before")
    @classmethod
    def validate_seniority(cls, v):
        if not v:
            return []
        if isinstance(v[0], SeniorityLevel):
            return v
        seniority_list = parse_seniority_list(v)
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


class JobCreate(BaseModel):
    url: str
    title: str
    description: str
    location: str
    country: str
    company: str
    source_website: str
    home_office: bool
    seniority_levels: list[SeniorityLevel]
