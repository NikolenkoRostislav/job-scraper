from pydantic import BaseModel, field_validator
from src.utils.parsers import parse_seniority_list, parse_skill_list, parse_country


class Filters(BaseModel):
    seniority: list[str]
    skills: list[str]
    country: str | None = None

    @field_validator("seniority", mode="before")
    @classmethod
    def validate_seniority(cls, v):
        seniority_list = parse_seniority_list(v or [], strict=True)
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

class SkillBase(BaseModel):
    id: int
    name: str
    category: str | None = None
    
    class Config:
        from_attributes = True

class JobBase(BaseModel):
    id: int
    title: str
    description: str | None = None
    location: str | None = None
    country: str | None = None
    seniority_levels: list[str] | None = None
    url: str
    
    class Config:
        from_attributes = True

class JobListResponse(BaseModel):
    jobs: list[JobBase]
    size: int

class SkillListResponse(BaseModel):
    skills: list[SkillBase]

class SkillDetailResponse(BaseModel):
    skill: SkillBase
    job_count: int