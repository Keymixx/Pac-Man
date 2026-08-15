from pydantic import BaseModel, Field, field_validator, ValidationError
from pathlib import Path
from typing import List

class LevelStructure(BaseModel):
    name: str=Field(min_length=1)
    width: int=Field(gt=2)
    heigh: int=Field(gt=2)


class Config(BaseModel):
    highscore_filename: str

    @field_validator('highscore_filename', mode='after')
    @classmethod
    def valid_file(cls, file_name: str):
        file_path = Path(file_name)
        if not file_path.exists():
            raise FileNotFoundError(f"{file_name} not found")
        elif not file_path.suffix == ".json":
            raise ValueError("Highscore file must be a JSON")
    lives: int = Field(gt=0)
    pacgum: int = Field(gt=0)
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    levels: List[LevelStructure]
