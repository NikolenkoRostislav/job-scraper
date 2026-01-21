from datetime import datetime
from sqlalchemy import DateTime, text
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base


class ScrapeReport(Base):
    __tablename__ = "scrape_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    target_website: Mapped[str]
    scrape_started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    scrape_finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    total_jobs_scraped: Mapped[int] = mapped_column(default=0)
    warnings_count: Mapped[int] = mapped_column(default=0)
    errors_count: Mapped[int] = mapped_column(default=0)
    end_reason: Mapped[str | None]