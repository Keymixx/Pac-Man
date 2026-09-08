from .config_loader import config_loader
from .models.config import ConfigFile
from .game import run_game
import sys
from mazegenerator import MazeGenerator

if __name__ == "__main__":
    try:
        config: ConfigFile = config_loader(sys.argv[1])
        print(config)
    except Exception as e:
        print(e)

    maze = MazeGenerator(
        size=(config.levels[0].width, config.levels[0].height),
        perfect=False
    )

    maze.generate()
    print(maze.maze)
    run_game(maze.maze)
