from sqlalchemy import ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base


class JobListing(Base):
    __tablename__ = "job_listings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    description: Mapped[str | None]
    location: Mapped[str | None]
    seniority_levels: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    url: Mapped[str] = mapped_column(unique=True)

    skills: Mapped[list["Skill"]] = relationship(
        "Skill",
        secondary="job_listing_skills",
        back_populates="job_listings",
        cascade="all, delete",
    )
