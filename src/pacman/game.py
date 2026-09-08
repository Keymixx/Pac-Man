import arcade
from .maze.maze_builder import build_maze

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
WINDOW_TITLE = "Pac-Man"

HUD_HEIGHT = 60
MAZE_AREA_HEIGHT = WINDOW_HEIGHT - HUD_HEIGHT


class GameView(arcade.Window):
    def __init__(self, maze: list[list[int]]):

        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.maze = maze
        self.background_color = arcade.csscolor.BLACK
        self.tiles_list = build_maze(
            self.maze, WINDOW_WIDTH, MAZE_AREA_HEIGHT, y_offset=HUD_HEIGHT
        )

        self.score = 0
        self.lives = 3
        self.level = 1
        self.time_remaining = 90

        self.score_text = arcade.Text(
            "Score: 0", 10, HUD_HEIGHT / 2, arcade.color.WHITE,
            16, anchor_y="center"
        )
        self.lives_text = arcade.Text(
            "Lives: 3", WINDOW_WIDTH / 2 - 200, HUD_HEIGHT / 2,
            arcade.color.WHITE, 16, anchor_y="center"
        )
        self.level_text = arcade.Text(
            "Level: 1", WINDOW_WIDTH / 2 + 60, HUD_HEIGHT / 2,
            arcade.color.WHITE, 16, anchor_y="center"
        )
        self.time_text = arcade.Text(
            "Time: 90", WINDOW_WIDTH - 120, HUD_HEIGHT / 2,
            arcade.color.WHITE, 16, anchor_y="center"
        )

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def update_hud(self):
        """Refresh HUD text objects from current game state."""
        self.score_text.text = f"Score: {self.score}"
        self.lives_text.text = f"Lives: {self.lives}"
        self.level_text.text = f"Level: {self.level}"
        self.time_text.text = f"Time: {self.time_remaining}"

    def on_update(self, delta_time: float):
        self.update_hud()

    def on_draw(self):
        """Render the screen."""
        self.clear()

        arcade.draw_lrbt_rectangle_filled(
            0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, arcade.color.BLACK
        )

        self.tiles_list.draw()

        self.score_text.draw()
        self.lives_text.draw()
        self.level_text.draw()
        self.time_text.draw()

    def on_key_press(self, key, key_modifiers):
        """Called whenever a key on the keyboard is pressed."""
        if key == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)


def run_game(maze: list[list[int]]):
    window = GameView(maze)
    window.setup()
    arcade.run()
