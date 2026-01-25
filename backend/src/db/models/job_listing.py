from datetime import datetime
from sqlalchemy import DateTime, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base
from src.db.types import seniority_level_enum
from src.utils.classes.enums import SeniorityLevel


class JobListing(Base):
    __tablename__ = "job_listings"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str]
    home_office: Mapped[bool | None] = mapped_column(default=False, index=True)
    description: Mapped[str | None]
    location: Mapped[str | None]
    country: Mapped[str | None] = mapped_column(index=True)
    company: Mapped[str | None]
    source_website: Mapped[str | None]
    seniority_levels: Mapped[list[SeniorityLevel] | None] = mapped_column(ARRAY(seniority_level_enum), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    last_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

    skills: Mapped[list["Skill"]] = relationship(
        "Skill",
        secondary="job_listing_skills",
        back_populates="job_listings",
    )
