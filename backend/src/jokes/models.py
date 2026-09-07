from pydantic import BaseModel, Field


class Joke(BaseModel):
    id: int | None = None
    setup: str = Field(min_length=1)
    punchline: str = Field(min_length=1)
    type: str
    category: str
