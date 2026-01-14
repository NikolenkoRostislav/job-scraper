from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    category: Mapped[str | None] = mapped_column(index=True)

    job_listings: Mapped[list["JobListing"]] = relationship(
        "JobListing",
        secondary="job_listing_skills",
        back_populates="skills",
    )
