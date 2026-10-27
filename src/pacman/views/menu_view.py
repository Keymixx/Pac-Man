import arcade

from typing import Any
from ..game import GameView, HUD_BORDER_COLOR
from ..highscore_loader import load_highscores
from ..maze.maze_factory import generate_maze
from ..models.config import ConfigFile


class MenuView(arcade.View):
    """Main menu: Start game / highscores / info on cheat mode and rules"""

    def __init__(self, config: ConfigFile) -> None:
        super().__init__()
        self.game_config = config
        self.background_color = arcade.color.BLACK

        w = self.window.width
        h = self.window.height

        self.texts: list[arcade.Text] = [
            arcade.Text("Pac-Man", w * 0.30, h - 100, arcade.color.YELLOW, 48,
                        anchor_x="center", bold=True),
            arcade.Text("Push SPACE to play", w * 0.30, h - 130,
                        arcade.color.WHITE, 18, anchor_x="center"),
            arcade.Text("Highscores:", w * 0.30, h - 180,
                        arcade.color.WHITE, 16, anchor_x="center", bold=True),
        ]

        highscores = load_highscores(config.highscore_filename)
        top = sorted(highscores.highscores,
                     key=lambda e: e.score, reverse=True)[:10]

        if not top:
            self.texts.append(
                arcade.Text("No score yet", w * 0.30, h - 215,
                            arcade.color.GRAY, 14, anchor_x="center"))
        for i, entry in enumerate(top):
            self.texts.append(
                arcade.Text(f"{i + 1}. {entry.name} - {entry.score} pts",
                            w * 0.30, h - 215 - i * 28,
                            arcade.color.WHITE, 14, anchor_x="center"))

        self.error_text = arcade.Text("", w / 2, 40, arcade.color.RED, 14,
                                      anchor_x="center")

        self.sprite_list: arcade.SpriteList = arcade.SpriteList()
        size = 50
        step = size + 8
        cx = w * 0.85
        cy = h * 0.30

        arrows = {
            "assets/hud/up.png": (0, 1),
            "assets/hud/left.png": (-1, 0),
            "assets/hud/down.png": (0, 0),
            "assets/hud/right.png": (1, 0),
        }
        for path, (col, row) in arrows.items():
            arrow = arcade.Sprite(path)
            ratio = arrow.height / arrow.width
            arrow.width = size
            arrow.height = size * ratio
            arrow.center_x = cx + col * step
            arrow.center_y = cy + row * step
            self.sprite_list.append(arrow)

        self._add_frame(105, 45, 170, 50)
        self.texts.append(arcade.Text(
            "EXIT", 105, 45, arcade.color.WHITE, 14,
            anchor_x="center", anchor_y="center"))

        cheat_lines = [
            "F1 = Cheat mode",
            "+ F = Freeze",
            "+ L = +1 Life",
            "+ I = Invu",
            "+ N = Next stage",
        ]
        line_h = 26
        pad = 14
        box_w = 200
        box_h = len(cheat_lines) * line_h + 2 * pad
        box_top = cy - 55

        self._add_frame(cx, box_top - box_h / 2, box_w, box_h)
        for i, line in enumerate(cheat_lines):
            color = arcade.color.RED if i == 0 else arcade.color.WHITE
            self.texts.append(arcade.Text(
                line, cx - box_w / 2 + pad,
                box_top - pad - line_h / 2 - i * line_h,
                color, 14, anchor_y="center"))

        rules_lines = [
            "RULES",
            "- Eat all the pacgums to",
            "  clear the level",
            "- Avoid the ghosts: each hit",
            "  costs one life",
            "- Eat a super-pacgum to make",
            "  ghosts edible for a while",
            "- Beat the clock on each level",
            "- Clear every level to win",
        ]
        rules_line_h = 24
        rules_pad = 14
        rules_w = 280
        rules_h = len(rules_lines) * rules_line_h + 2 * rules_pad
        rules_cx = w - 20 - rules_w / 2
        rules_top = h - 20

        self._add_frame(rules_cx, rules_top - rules_h / 2, rules_w, rules_h)
        for i, line in enumerate(rules_lines):
            color = arcade.color.YELLOW if i == 0 else arcade.color.WHITE
            self.texts.append(arcade.Text(
                line, rules_cx - rules_w / 2 + rules_pad,
                rules_top - rules_pad - rules_line_h / 2 - i * rules_line_h,
                color, 13, anchor_y="center", bold=(i == 0)))

    def _add_frame(self, center_x: float, center_y: float,
                   width: float, height: float) -> None:
        """Add a rectangle with a blue border and a black inside."""
        border = arcade.SpriteSolidColor(
            int(width), int(height), color=HUD_BORDER_COLOR)
        border.center_x = center_x
        border.center_y = center_y

        inside = arcade.SpriteSolidColor(
            int(width) - 4, int(height) - 4, color=arcade.color.BLACK)
        inside.center_x = center_x
        inside.center_y = center_y

        self.sprite_list.append(border)
        self.sprite_list.append(inside)

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

        self.sprite_list.draw()
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

    def on_mouse_press(self, x: int, y: int,
                       button: Any, modifiers: Any) -> None:
        btn_x, btn_y, btn_w, btn_h = 105, 45, 170, 50
        if (btn_x - btn_w / 2 <= x <= btn_x + btn_w / 2 and
                btn_y - btn_h / 2 <= y <= btn_y + btn_h / 2):
            arcade.close_window()
