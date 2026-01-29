from pydantic import BaseModel


class SkillBase(BaseModel):
    id: int
    name: str
    category: str | None = None

    class Config:
        from_attributes = True


class SkillDetailResponse(BaseModel):
    skill: SkillBase
    job_count: int

    
class SkillListResponse(BaseModel):
    skills: list[SkillDetailResponse]
