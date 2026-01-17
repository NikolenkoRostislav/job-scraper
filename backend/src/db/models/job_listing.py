from datetime import datetime
from sqlalchemy import ARRAY, String, Boolean, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base


class JobListing(Base):
    __tablename__ = "job_listings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    url: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str]
    home_office: Mapped[bool | None] = mapped_column(default=False)
    description: Mapped[str | None]
    location: Mapped[str | None]
    country: Mapped[str | None]
    company: Mapped[str | None]
    source_website: Mapped[str | None]
    seniority_levels: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    last_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

    skills: Mapped[list["Skill"]] = relationship(
        "Skill",
        secondary="job_listing_skills",
        back_populates="job_listings",
        cascade="all, delete",
    )
