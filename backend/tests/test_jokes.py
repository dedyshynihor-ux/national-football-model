import sys
from pathlib import Path

import httpx
import pytest
from fastapi import FastAPI

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from jokes.router import router, service
from jokes.service import JokeService


@pytest.mark.asyncio
async def test_service_caches_a_joke():
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(
            200,
            json={"id": 1, "setup": "Why?", "punchline": "Because.", "type": "general"},
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url="https://test"
    ) as client:
        joke_service = JokeService(client)
        assert (await joke_service.get_random_joke()).setup == "Why?"
        await joke_service.get_random_joke()
    assert calls == 1


@pytest.mark.asyncio
async def test_service_retries_then_raises():
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(503)

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url="https://test"
    ) as client:
        with pytest.raises(RuntimeError):
            await JokeService(client).get_random_joke()
    assert calls == 3


@pytest.mark.asyncio
async def test_service_uses_first_joke_from_category_response():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/jokes/programming/ten"
        return httpx.Response(
            200,
            json=[
                {
                    "id": 3,
                    "setup": "Why do programmers prefer dark mode?",
                    "punchline": "Because light attracts bugs.",
                    "type": "programming",
                }
            ],
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url="https://test"
    ) as client:
        joke = await JokeService(client).get_random_joke("programming")
    assert joke.category == "programming"
    assert joke.id == 3


@pytest.mark.asyncio
async def test_random_endpoint_returns_service_joke(monkeypatch):
    async def fake_get_random_joke(category=None):
        return {"id": 2, "setup": "Setup", "punchline": "Punchline", "type": "general", "category": "general"}

    monkeypatch.setattr(service, "get_random_joke", fake_get_random_joke)
    app = FastAPI()
    app.include_router(router)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/jokes/random")
    assert response.status_code == 200
    assert response.json()["punchline"] == "Punchline"
