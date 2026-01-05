from sqlalchemy.ext.asyncio import AsyncSession


class SkillService:
    @staticmethod
    async def get_top_skills(limit: int, db: AsyncSession):
        pass

    @staticmethod
    async def get_skill_by_name(skill_name: str, db: AsyncSession):
        pass
