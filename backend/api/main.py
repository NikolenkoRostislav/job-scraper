import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import text

from api.middleware import timing_middleware
from api.exception_handler import error_handlers
from api.routes import job_router, skill_router, auth_router, user_router, admin_router, favorited_job_router
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


app = FastAPI(
    root_path="/api", 
    title=settings.app.APP_NAME, 
    debug=settings.app.DEBUG, 
    lifespan=lifespan,
    docs_url="/docs" if settings.app.DEBUG else None,
    redoc_url="/redoc" if settings.app.DEBUG else None,
    openapi_url="/openapi.json" if settings.app.DEBUG else None,
)

if settings.app.DEBUG:
    origins = settings.app.ALLOWED_ORIGINS_DEV
else:
    origins = settings.app.ALLOWED_ORIGINS_PROD

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.auth.SESSION_SECRET_KEY,
    https_only=not settings.app.DEBUG,
    max_age=3600
)

timing_middleware(app)

error_handlers(app)

routers = [
    auth_router,
    user_router, 
    skill_router,
    job_router, 
    favorited_job_router,
    admin_router
]

for router in routers:
    app.include_router(router)


@app.get("/health")
async def check_health(db: DatabaseDep):
    try:
        await get_redis().ping()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Redis unhealthy: {e}")

    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unhealthy: {e}")

    return {"api_healthy": True}
