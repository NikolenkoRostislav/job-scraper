from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]
    APP_NAME: str = "JobScraper"
    DEBUG: bool = True

    DATABASE_URL: str
    CELERY_BROKER_URL: str
    GLOBAL_SCRAPE_PAGINATION_LIMIT: int = 30
    SCHEDULED_SCRAPE_DELAY_HOURS: int = 3

    SKILL_MAPPINGS_FILENAME: str = "skill_mappings.json"
    COUNTRY_MAPPINGS_FILENAME: str = "country_mappings.json"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14

    GOOGLE_OAUTH_CLIENT_ID: str
    GOOGLE_OAUTH_CLIENT_SECRET: str
    FRONTEND_REDIRECT_URL: str
    GOOGLE_CALLBACK_URL: str
    SESSION_SECRET_KEY: str

    ALGORITHM: str = "HS256"
    SECRET_KEY: str

    EMAIL_DOMAIN: str = "smtp.gmail.com"
    EMAIL_PORT: int = 465
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    EMAIL_CODE_TTL_MINUTES: int = 15

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
