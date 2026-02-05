from functools import lru_cache

from redis.asyncio import Redis

from core.config import settings


@lru_cache
def get_redis() -> Redis:
    return Redis(host=settings.redis.REDIS_HOST, port=settings.redis.REDIS_PORT)