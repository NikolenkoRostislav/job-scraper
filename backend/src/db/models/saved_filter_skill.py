from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base


class SavedFilterSkill(Base):
    __tablename__ = "saved_filter_skills"

    saved_filter_id: Mapped[int] = mapped_column(
        ForeignKey("saved_filters.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True, index=True
    )
