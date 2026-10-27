*This project has been created as part of the 42 curriculum by caaubert and mterrier.*

# Pac-Man

---

## Description
This project is a fully-featured, modernized clone of the classic **Pac-Man** arcade game, developed in Python using the **Arcade** library. The primary goal is to provide an engaging arcade experience featuring multiple progressive levels, custom maze generation, intelligent ghost entities (Blinky, Pinky, Inky, Clyde) with distinct states (chase, scatter, frightened, and respawn), a highscore tracking system, and robust configuration parsing. 

Key features include:
* **Multiple Levels:** Progressive level configurations with dynamic dimensions.
* **Ghost AI & Mechanics:** Advanced pathfinding using BFS for eyes returning to spawn, and frightened states when super pac-gums are consumed.
* **Cheat & Debug Modes:** Built-in development controls for testing and demonstration.
* **Custom Configuration:** Strict validation using Pydantic with inline comment support.

---

## Instructions

### Prerequisites
Make sure you have Python 3.10+ and `uv` installed on your system.

### Installation & Execution
You can easily build, run, and test the project using the provided **Makefile**:

```bash
# Install dependencies
make install

# Run the game with the default configuration
make run

# Run code style checks and linters
make lint

# Clean temporary cache files
make clean
```

You can also run the main script directly via `uv`:
```bash
uv run python3 -m pacman.main config.json
```

---

## Configuration
The game is configured via a JSON file (`config.json`) located at the root of the project. 

### Features & Structure
* **Comment Support:** Lines starting with `#` are automatically filtered out and ignored during loading.
* **Validation:** Powered by **Pydantic** (`ConfigFile` model), ensuring all fields (such as `lives`, `levels`, dimensions, and points) are strictly validated. If a configuration error occurs, a clean, human-readable error message is displayed without a Python traceback.

### Example Configuration Fields
* `lives`: Initial number of lives for the player.
* `percent_pacgum`: Density of standard pac-gums.
* `points_per_pacgum`, `points_per_super_pacgum`, `points_per_ghost`: Scoring metrics.
* `levels`: An array of level configurations specifying each level's width, height, and maximum duration (`level_max_time`).

---

## Highscore
The highscore system tracks and persists top player scores across game sessions. 
* **Design Choice:** Highscores are decoupled from the main game loop via a dedicated loader (`highscore_loader.py`) and model (`highscore.py`). This separation ensures clean code architecture, making it easy to read, update, and validate score logs without bloating view or game logic classes.

---

## Maze Generation
Mazes are procedurally generated for each level using the custom bundled wheel package **`mazegenerator`** located in the `libs/` directory.
* **Integration:** `maze_builder.py` and `maze_factory.py` interface with the package using the dimensions defined in the active level configuration (`level.width` and `level.height`). The resulting matrix is converted into Arcade sprite tiles and interactable collision boundaries.

---

## Implementation
The project follows a clean, modular, and object-oriented architecture built around the **Arcade View Management** system:
* **Views:** Separated into distinct screens (`MenuView`, `GameView`, `PauseView`, `EndView`).
* **Entities:** Modular classes handling player movement/animation (`Player`), ghost state machines/pathfinding (`Ghost`), and collection management (`PacgumList`).
* **Error Handling:** Graceful catching of configuration errors and file issues using explicit exception blocks (`ValidationError`, `FileNotFoundError`, `json.JSONDecodeError`) to ensure user-friendly terminal outputs.

---

## General Software Architecture
The source code is organized inside the `src/pacman/` package following a strict separation of concerns:

```text
src/pacman/
├── main.py              # Application entry point and exception handler
├── game.py              # Core game loop and View controller
├── config_loader.py     # JSON reader with comment filtering and Pydantic validation
├── highscore_loader.py  # Highscore management
├── entities/            # Game characters and collectibles (player, ghost, pacgum)
├── maze/                # Maze generation factories and builders
├── models/              # Pydantic data models (config, highscore)
└── views/               # Screen views (menu, pause, end game)
```

---

## Project Management
The project was managed using an agile-inspired Kanban methodology to track tasks, feature implementations, and bug fixes. 

You can view the project board snapshot and workflow structure in the dedicated management directory:
* **Linear:** [management/Pac-Man KanBan1.png](management/Pac-Man KanBan1.png)

---

## Resources & AI Usage

### References & Documentation
* [Python Arcade Library Documentation](https://api.arcade.academy/)
* [Pydantic Documentation](https://docs.pydantic.dev/)
* Classic Pac-Man Game Mechanics & Ghost Behavior Guidelines

### AI Usage Disclosure
AI tools were used collaboratively during the development of this project for the following tasks and components:

* **Code Refactoring & Linting:** Optimizing `mypy` type annotations and structuring clean error-handling blocks for Pydantic validation.
* **Documentation:** Assisting in structuring and drafting this `README.md` file according to the curriculum requirements.