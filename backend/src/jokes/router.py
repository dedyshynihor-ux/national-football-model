from fastapi import APIRouter, HTTPException, Request

from .models import Joke
from .service import JokeService

router = APIRouter(prefix="/api/v1/jokes", tags=["jokes"])
service = JokeService()


@router.get("/random", response_model=Joke, summary="Get a random joke")
async def random_joke(request: Request) -> Joke:
    return await _get_joke()


@router.get("/category/{category}", response_model=Joke, summary="Get a category joke")
async def category_joke(category: str, request: Request) -> Joke:
    return await _get_joke(category)


async def _get_joke(category: str | None = None) -> Joke:
    try:
        return await service.get_random_joke(category)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
