import json
from .models.highscore import HighscoreFile


def load_highscores(path: str) -> HighscoreFile:
    """Load the highscore file, or an empty list if it cannot be used."""
    try:
        with open(path, "r") as f:
            raw = json.load(f)
        return HighscoreFile.model_validate(raw)
    except FileNotFoundError:
        return HighscoreFile()
    except (OSError, ValueError) as e:
        print(f"Warning: cannot use '{path}' ({type(e).__name__}), "
              "starting with an empty highscore list.")
        return HighscoreFile()
