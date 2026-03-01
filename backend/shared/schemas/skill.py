from pydantic import BaseModel, computed_field


class SkillBase(BaseModel):
    id: int
    name: str
    category: str | None = None

    class Config:
        from_attributes = True


class SkillDetailResponse(BaseModel):
    skill: SkillBase
    job_count: int
    frequency: float


class SkillListResponse(BaseModel):
    skills: list[SkillDetailResponse]

    @computed_field
    @property
    def size(self) -> int:
        return len(self.skills)
