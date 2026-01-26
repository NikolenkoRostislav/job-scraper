import logging
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from src.api.middleware import TimingMiddleware
from src.api.routes import job_router, skill_router, auth_router, user_router, admin_router
from src.config import settings
from src.db.models import *
from src.utils.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(log_file="api.log")
    logger = logging.getLogger(__name__)
    logger.info("API server started")
    yield


app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)

origins = settings.ALLOWED_ORIGINS

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

app.add_middleware(TimingMiddleware)

app.include_router(skill_router)
app.include_router(job_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(admin_router)

if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
