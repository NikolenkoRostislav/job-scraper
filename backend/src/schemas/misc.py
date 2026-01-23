from datetime import datetime, timezone
from pydantic import BaseModel, field_validator


class DateRange(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None

    @field_validator("end_time", mode="before")
    def validate_end_time(cls, v):
        if not v:
            return datetime.now(timezone.utc)


class WebsiteStats(BaseModel):
    job_count: int
    scrape_count: int
    date_range: DateRange
