from pydantic import BaseModel


class SkillBase(BaseModel):
    id: int
    name: str
    category: str | None = None

    class Config:
        from_attributes = True


class SkillListResponse(BaseModel):
    skills: list[SkillBase]


class SkillDetailResponse(BaseModel):
    skill: SkillBase
    job_count: int
