from fastapi import APIRouter, Path

from src.services import SkillService
from src.schemas import SkillListResponse, SkillDetailResponse
from src.api.dependencies import DatabaseDep
from src.api.exception_handler import handle_exceptions


SKILL_RANKING_MAX = 50
router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("/ranking/{limit}", response_model=SkillListResponse)
@handle_exceptions
async def get_skills(db: DatabaseDep, limit: int = Path(le=SKILL_RANKING_MAX)):
    return await SkillService.get_top_skills(limit, db)


@router.get("/{skill_name}", response_model=SkillDetailResponse | None)
@handle_exceptions
async def get_skill(db: DatabaseDep, skill_name: str):
    return await SkillService.get_skill_by_name(skill_name, db)
