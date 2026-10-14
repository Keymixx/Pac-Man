from pydantic import BaseModel, Field
from typing import List


class HighscoreEntry(BaseModel):
    name: str = Field(min_length=1, max_length=10, pattern=r"^[A-Za-z0-9 ]+$")
    score: int = Field(ge=0)


class HighscoreFile(BaseModel):
    highscores: List[HighscoreEntry] = []
