import arcade

from ..game import GameView
from ..highscore_loader import load_highscores
from ..maze.maze_factory import generate_maze
from ..models.config import ConfigFile


class MenuView(arcade.View):
    """Main menu: Pacamn / space to start / highscores"""

    def __init__(self, config: ConfigFile) -> None:
        super().__init__()
        self.game_config = config
        self.background_color = arcade.color.BLACK

        w = self.window.width
        h = self.window.height

        self.texts: list[arcade.Text] = [
            arcade.Text("Pac-Man", w / 2, h - 150, arcade.color.YELLOW, 48,
                        anchor_x="center", bold=True),
            arcade.Text("Push SPACE to play", w / 2, h - 230,
                        arcade.color.WHITE, 18, anchor_x="center"),
            arcade.Text("Highscores:", w / 2, h - 320,
                        arcade.color.WHITE, 16, anchor_x="center", bold=True),
        ]

        highscores = load_highscores(config.highscore_filename)
        top = sorted(highscores.highscores,
                     key=lambda e: e.score, reverse=True)[:10]

        if not top:
            self.texts.append(
                arcade.Text("No score yet", w / 2, h - 355,
                            arcade.color.GRAY, 14, anchor_x="center"))
        for i, entry in enumerate(top):
            self.texts.append(
                arcade.Text(f"{i + 1}. {entry.name} - {entry.score} pts",
                            w / 2, h - 355 - i * 28,
                            arcade.color.WHITE, 14, anchor_x="center"))

        self.error_text = arcade.Text("", w / 2, 40, arcade.color.RED, 14,
                                      anchor_x="center")

    def _start_game(self) -> None:
        """Generate the first maze and switch to the game view."""
        level = self.game_config.levels[0]
        try:
            maze = generate_maze(level.width, level.height)
        except Exception as e:
            self.error_text.text = f"Maze generation failed: {e}"
            return
        self.window.show_view(GameView(maze, self.game_config))

    def on_draw(self) -> None:
        self.clear()
        for text in self.texts:
            text.draw()
        self.error_text.draw()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.SPACE:
            self._start_game()
        elif key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
