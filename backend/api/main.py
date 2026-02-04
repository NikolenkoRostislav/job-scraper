import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import text

from api.middleware import timing_middleware, username_extraction_middleware
from api.exception_handler import error_handlers
from api.routes import job_router, skill_router, auth_router, user_router, admin_router
from api.dependencies import DatabaseDep
from core.config import settings
from core.redis import get_redis
from shared.models import *
from shared.utils import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(log_file="api.log")
    redis = get_redis()
    logger = logging.getLogger(__name__)
    logger.info("API server started")
    yield
    await redis.aclose()


app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)

if settings.DEBUG:
    origins = settings.ALLOWED_ORIGINS_DEV
else:
    origins = settings.ALLOWED_ORIGINS_PROD

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    https_only=not settings.DEBUG,
    max_age=3600
)

timing_middleware(app)
username_extraction_middleware(app) # Used for rate limiting login attempts by username

error_handlers(app)

app.include_router(skill_router)
app.include_router(job_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(admin_router)

@app.get("/health")
async def check_health(db: DatabaseDep):
    redis_healthy = True
    try:
        await get_redis().ping()
    except:
        redis_healthy = False

    db_healthy = True
    try:
        await db.execute(text("SELECT 1"))
    except:
        db_healthy = False

    return {"api_healthy": True, "db_healthy": db_healthy, "redis_healthy": redis_healthy}

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
