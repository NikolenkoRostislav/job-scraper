from fastapi import APIRouter, Path

from shared.services import SkillService
from shared.schemas import SkillListResponse, SkillDetailResponse
from api.dependencies import DatabaseDep


SKILL_RANKING_MAX = 50
router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("/ranking/{limit}", response_model=SkillListResponse)
async def get_skills(db: DatabaseDep, limit: int = Path(le=SKILL_RANKING_MAX)):
    return await SkillService.get_top_skills(db, limit=limit)


@router.get("/{skill_name}", response_model=SkillDetailResponse | None)
async def get_skill(db: DatabaseDep, skill_name: str):
    return await SkillService.get_skill_by_name(db, skill_name)
