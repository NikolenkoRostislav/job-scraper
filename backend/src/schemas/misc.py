from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, field_validator


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
    date_range: DateRange


class LogEntry(BaseModel):
    timestamp: datetime
    level: str
    source: str
    message: str


class Email(BaseModel):
    receiver: EmailStr


class SendEmail(Email):
    subject: str
    content: str # This content is only shown if the email client doesn't support html or no html content is provided
    html_content: str | None = None
