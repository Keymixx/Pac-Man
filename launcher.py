import os
import runpy
import sys
from pathlib import Path

import pacman.main  # noqa: F401  (pour que PyInstaller détecte le package)


def main() -> None:
    if getattr(sys, "frozen", False):
        # Assets, config.json et highscore.json vivent à côté de l'exécutable
        os.chdir(Path(sys.executable).parent)
    sys.argv = ["pacman", "config.json"]
    runpy.run_module("pacman.main", run_name="__main__")


if __name__ == "__main__":
    main()
