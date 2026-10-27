import os
import runpy
import sys
from pathlib import Path

import pacman.main


def main() -> None:
    if getattr(sys, "frozen", False):
        os.chdir(Path(sys.executable).parent)
    sys.argv = ["pacman", "config.json"]
    runpy.run_module("pacman.main", run_name="__main__")


if __name__ == "__main__":
    main()
