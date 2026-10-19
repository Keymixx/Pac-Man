import sys

import arcade

from .config_loader import config_loader
from .game import WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from .models.config import ConfigFile
from .views.menu_view import MenuView

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py config.json")
        sys.exit(1)

    try:
        config: ConfigFile = config_loader(sys.argv[1])
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

    try:
        window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        window.show_view(MenuView(config))
        arcade.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
        sys.exit(0)
