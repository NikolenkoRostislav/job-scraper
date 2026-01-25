from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base
from src.db.types import seniority_level_enum
from src.utils.classes.enums import SeniorityLevel


class SavedFilter(Base):
    __tablename__ = "saved_filters"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)
    seniority: Mapped[list[SeniorityLevel] | None] = mapped_column(ARRAY(seniority_level_enum), nullable=True)
    country: Mapped[str | None] = mapped_column(index=True)
    company: Mapped[str | None] = mapped_column(index=True)

    skills: Mapped[list["Skill"]] = relationship(
        "Skill",
        secondary="saved_filter_skills",
        back_populates="saved_filters",
    )
