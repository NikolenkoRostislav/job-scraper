from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]
    APP_NAME: str = "JobScraper"
    DEBUG: bool = True
    DATABASE_URL: str
    CELERY_BROKER_URL: str
    GLOBAL_SCRAPE_PAGINATION_LIMIT: int = 30
    SKILL_MAPPINGS_FILENAME: str = "skill_mappings.json"
    COUNTRY_MAPPINGS_FILENAME: str = "country_mappings.json"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14

    ALGORITHM: str = "HS256"
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
