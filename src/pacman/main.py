from .config_loader import config_loader
from .models.config import ConfigFile
from .game import run_game
import sys
from mazegenerator import MazeGenerator

if __name__ == "__main__":
    try:
        config: ConfigFile = config_loader(sys.argv[1])
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

    try:
        maze = MazeGenerator(
            size=(config.levels[0].width, config.levels[0].height),
            perfect=False
        )
        maze.generate()
    except Exception as e:
        print(f"Error generating maze: {e}")
        sys.exit(1)

    try:
        print(maze.maze)
        run_game(maze.maze, config)
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
        sys.exit(0)
