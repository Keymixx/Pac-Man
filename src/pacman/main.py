import sys

import arcade
import json

from pydantic import ValidationError
from .config_loader import config_loader
from .game import WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from .models.config import ConfigFile
from .views.menu_view import MenuView

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py config.json")
        sys.exit(1)

    config_path = sys.argv[1]

    try:
        config: ConfigFile = config_loader(config_path)
    except PermissionError:
        print(f"Permission missing to open {config_path}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"File {config_path} doesn't exist")
        sys.exit(1)
    except KeyError as e:
        print(f"KeyError: {e}")
        sys.exit(1)
    except ValidationError as e:
        err = e.errors()[0]
        field_path = ".".join(str(x) for x in err['loc'])
        print(f"Error : Field '{field_path}' missing or invalid.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error : {e}")
        sys.exit(1)

    try:
        window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        window.show_view(MenuView(config))
        arcade.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
        sys.exit(0)
