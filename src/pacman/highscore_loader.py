import json

from .models.highscore import HighscoreEntry, HighscoreFile

MAX_HIGHSCORES = 10


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


def add_highscore(highscores: HighscoreFile, name: str,
                  score: int) -> HighscoreFile:
    """Return a new list with the entry added, sorted, cut to the top 10."""
    entries = highscores.highscores + [HighscoreEntry(name=name, score=score)]
    entries.sort(key=lambda e: e.score, reverse=True)
    return HighscoreFile(highscores=entries[:MAX_HIGHSCORES])


def save_highscores(path: str, highscores: HighscoreFile) -> bool:
    """Write the highscores to disk. Return False if it fails."""
    try:
        with open(path, "w") as f:
            json.dump(highscores.model_dump(), f, indent=4)
    except OSError as e:
        print(f"Warning: cannot save highscores to '{path}': {e}")
        return False
    return True
