import asyncio
import os
import logging
from random import choice
from typing import Any

import httpx
from redis import asyncio as redis
from pydantic import TypeAdapter

from .models import Joke

logger = logging.getLogger(__name__)

API_URL = "https://official-joke-api.appspot.com"
CACHE_TTL_SECONDS = 60 * 60
joke_list_adapter = TypeAdapter(list[Joke])


class JokeService:
    def __init__(
        self,
        client: httpx.AsyncClient | None = None,
        cache: redis.Redis | None = None,
    ) -> None:
        self._client = client
        self._cache: dict[str, tuple[float, list[Joke]]] = {}
        self._redis = cache or (
            redis.from_url(os.environ["REDIS_URL"], decode_responses=True)
            if os.getenv("REDIS_URL")
            else None
        )

    async def get_random_joke(self, category: str | None = None) -> Joke:
        cache_key = category or "random"
        redis_key = f"joke:{cache_key}"
        if self._redis:
            try:
                cached_joke = await self._redis.get(redis_key)
                if cached_joke:
                    return choice(joke_list_adapter.validate_json(cached_joke))
            except (redis.RedisError, ValueError) as error:
                logger.warning("Redis cache unavailable: %s", error)

        cached = self._cache.get(cache_key)
        now = asyncio.get_running_loop().time()
        if cached and cached[0] > now:
            return choice(cached[1])

        path = f"/jokes/{category}/ten" if category else "/random_ten"
        jokes = await self._fetch(path, category)
        self._cache[cache_key] = (now + CACHE_TTL_SECONDS, jokes)
        if self._redis:
            try:
                await self._redis.setex(
                    redis_key, CACHE_TTL_SECONDS, joke_list_adapter.dump_json(jokes)
                )
            except redis.RedisError as error:
                logger.warning("Unable to cache joke in Redis: %s", error)
        return choice(jokes)

    async def _fetch(self, path: str, requested_category: str | None) -> list[Joke]:
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                if self._client:
                    response = await self._client.get(path)
                else:
                    async with httpx.AsyncClient(
                        base_url=API_URL, timeout=0.5
                    ) as client:
                        response = await client.get(path)
                response.raise_for_status()
                payload: Any = response.json()
                jokes = payload if isinstance(payload, list) else [payload]
                if not jokes:
                    raise ValueError("Joke API returned no jokes")
                return [
                    Joke(
                        id=joke.get("id"),
                        setup=joke["setup"],
                        punchline=joke["punchline"],
                        type=joke.get("type", "unknown"),
                        category=requested_category or joke.get("type", "general"),
                    )
                    for joke in jokes
                ]
            except (httpx.HTTPError, AttributeError, KeyError, ValueError) as error:
                last_error = error
                logger.warning("Joke API attempt %s failed: %s", attempt + 1, error)
                if attempt < 2:
                    await asyncio.sleep(0.1 * (attempt + 1))
        raise RuntimeError("Joke service is temporarily unavailable") from last_error
