from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    APP_NAME: str = "JobScraper"
    DEBUG: bool = True
    ALLOWED_ORIGINS_DEV: list[str] = ["http://localhost:5173"]
    ALLOWED_ORIGINS_PROD: list[str] = []


class ScrapeSettings(BaseModel):
    GLOBAL_SCRAPE_PAGINATION_LIMIT: int = 300
    SCHEDULED_SCRAPE_DELAY_HOURS: int = 24
    SCHEDULED_CLEANUP_DELAY_HOURS: int = 48


class FileSettings(BaseModel):
    SKILL_MAPPINGS_FILENAME: str = "skill_mappings.json"
    COUNTRY_MAPPINGS_FILENAME: str = "country_mappings.json"


class RedisSettings(BaseModel):
    REDIS_PORT: int = 6379
    REDIS_HOST: str = "localhost"


class DatabaseSettings(BaseModel):
    DB_USER: str = "postgres"
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "jobscraper"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class CelerySettings(BaseModel):
    CELERY_BROKER_URL: str


class AuthSettings(BaseModel):
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14
    TOKEN_SECRET_KEY: str
    GOOGLE_OAUTH_CLIENT_ID: str
    GOOGLE_OAUTH_CLIENT_SECRET: str
    FRONTEND_REDIRECT_URL: str
    GOOGLE_CALLBACK_URL: str
    SESSION_SECRET_KEY: str


class EmailSettings(BaseModel):
    EMAIL_DOMAIN: str = "smtp.gmail.com"
    EMAIL_PORT: int = 465
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    EMAIL_CODE_TTL_MINUTES: int = 15


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    app: AppSettings = AppSettings()
    scrape: ScrapeSettings = ScrapeSettings()
    files: FileSettings = FileSettings()
    redis: RedisSettings = RedisSettings()
    database: DatabaseSettings
    celery: CelerySettings
    auth: AuthSettings
    email: EmailSettings


settings = Settings()
