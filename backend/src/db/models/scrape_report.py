from datetime import datetime, timezone
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base


class ScrapeReport(Base):
    __tablename__ = "scrape_reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    target_website: Mapped[str]
    scrape_started_at: Mapped[datetime | None]
    scrape_finished_at: Mapped[datetime | None]
    total_jobs_scraped: Mapped[int] = mapped_column(default=0)
