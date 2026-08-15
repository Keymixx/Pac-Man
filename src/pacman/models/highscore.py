from pydantic import Basemodel, Field
from typing import List

class HighscoreEntry(Basemodel):
    name: str = Field(max_length=3, pattern=r"/^[\w\-\s]+$/")
    scores: int = Field(gt=0)

class HighscoreFile(Basemodel):
    HigscoreList: List[HighscoreEntry]