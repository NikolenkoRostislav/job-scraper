from pydantic import BaseModel, field_validator
from src.utils.parsers import parse_seniority_list, parse_skill_list


class Filters(BaseModel):
    seniority: list[str]
    skills: list[str]

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