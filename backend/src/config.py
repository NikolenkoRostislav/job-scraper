from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]
    APP_NAME: str = "JobScraper"
    DEBUG: bool = True
    DATABASE_URL: str
    CELERY_BROKER_URL: str
    GLOBAL_SCRAPE_PAGINATION_LIMIT: int = 30

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
