# Code based on Artem Shumeiko's rate limiter: https://github.com/artemonsh/rate-limiter-fastapi-redis

from functools import lru_cache
from time import time
import random
from typing import Annotated, Callable

from redis.asyncio import Redis
from fastapi import Request, HTTPException, status, Depends

from api.dependencies import get_username
from core.redis import get_redis
from core.config import settings


class RateLimiter:
    def __init__(self, redis: Redis):
        self._redis = redis
        self._lua_sha = None

    async def _load_script(self):
        if self._lua_sha is None:
            # Removes old requests then checks if requests_in_window >= limit, rejects request if true, records the request and approves it if false
            script = """
            redis.call("ZREMRANGEBYSCORE", KEYS[1], 0, ARGV[2])
            local count = redis.call("ZCARD", KEYS[1])
            if count >= tonumber(ARGV[3]) then
                return 1
            end
            redis.call("ZADD", KEYS[1], ARGV[1], ARGV[5])
            redis.call("EXPIRE", KEYS[1], ARGV[4])
            return 0
            """
            self._lua_sha = await self._redis.script_load(script)

    async def is_limited(
        self,
        identifier: str,
        endpoint: str,
        max_requests: int,
        window_seconds: int,
    ) -> bool:
        await self._load_script()

        key = f"rate_limiter:{endpoint}:{identifier}"

        current_ms = int(time() * 1000)
        window_start_ms = current_ms - window_seconds * 1000
        member_id = f"{current_ms}-{random.randint(0, 100_000)}"

        result = await self._redis.evalsha(
            self._lua_sha,
            1,
            key,  # KEYS[1]
            current_ms,  # ARGV[1]
            window_start_ms,  # ARGV[2]
            max_requests,  # ARGV[3]
            window_seconds,  # ARGV[4]
            member_id,  # ARGV[5], prevents duplicate items in the sorted set
        )

        return result == 1


@lru_cache
def _get_rate_limiter() -> RateLimiter:
    return RateLimiter(get_redis())


def rate_limiter_factory(
    endpoint: str,
    max_requests: int,
    window_seconds: int,
    identifier_getter: Callable | None = None,
):
    async def dependency(
        request: Request,
        rate_limiter: Annotated[RateLimiter, Depends(_get_rate_limiter)],
    ):
        identifier = (
            identifier_getter(request) if identifier_getter else request.client.host
        )

        limited = await rate_limiter.is_limited(
            identifier,
            endpoint,
            max_requests,
            window_seconds,
        )

        if limited and not settings.app.DEBUG:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Request limit exceeded for this endpoint, please try again later",
            )

    return dependency


# Rate limiter dependencies
rate_limit_token_by_ip = rate_limiter_factory("token", 3, 60)
rate_limit_token_by_username = rate_limiter_factory(
    "token",
    3,
    60,
    identifier_getter=lambda req, username=Depends(get_username): username,
)
