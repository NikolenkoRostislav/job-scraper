from datetime import datetime, timezone
from pydantic import BaseModel, field_validator


class DateRange(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None

    @field_validator("end_time", mode="before")
    def validate_end_time(cls, v):
        if not v:
            return datetime.now(timezone.utc)
        return v


class ScrapeReport(BaseModel):
    id: int
    target_website: str
    scrape_started_at: datetime | None = None
    scrape_finished_at: datetime | None = None
    total_jobs_scraped: int = 0
    warnings_count: int = 0
    errors_count: int = 0
    end_reason: str | None = None

    class Config:
        from_attributes = True


class WebsiteStats(BaseModel):
    job_count: int
    scrape_count: int
    failed_scrape_count: int
    scrape_reports: list[ScrapeReport]
    date_range: DateRange
