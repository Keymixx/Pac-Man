import arcade
from .maze.maze_builder import build_maze
from .models.config import ConfigFile
# from .entities.player import Player

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Pac-Man"
MAZE_COLOR = arcade.csscolor.BLACK

PADS = (20, 20, 20, 20)
HUD_HEIGHT = 60
BORDER_THICKNESS = 1
HUD_BORDER_COLOR = (25, 60, 150)
PAD = (20,20,20,20)
MAZE_AREA_HEIGHT = WINDOW_HEIGHT - HUD_HEIGHT


class GameView(arcade.Window):
    def __init__(self, maze: list[list[int]], config: ConfigFile):

        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.maze = maze
        self.game_config = config
        self.background_color = MAZE_COLOR
        self.tiles_list, self.tile_size = build_maze(
            self.maze, WINDOW_WIDTH, MAZE_AREA_HEIGHT, height_hud=HUD_HEIGHT
        )

        self.hud_border = arcade.SpriteSolidColor(
            WINDOW_WIDTH, HUD_HEIGHT, color=HUD_BORDER_COLOR
        )
        self.hud_border.center_x = WINDOW_WIDTH / 2
        self.hud_border.center_y = HUD_HEIGHT / 2

        self.hud_background = arcade.Sprite("assets/hud/hud_background.png")
        self.hud_background.width = WINDOW_WIDTH - (2 * BORDER_THICKNESS)
        self.hud_background.height = HUD_HEIGHT - (2 * BORDER_THICKNESS)
        self.hud_background.center_x = WINDOW_WIDTH / 2
        self.hud_background.center_y = HUD_HEIGHT / 2

        self.hud_sprite_list = arcade.SpriteList()
        self.hud_sprite_list.append(self.hud_border)
        self.hud_sprite_list.append(self.hud_background)

        self.current_level_index = 0
        self.score = 0 
        self.lives = config.lives
        self.level = self.current_level_index + 1
        self.time_remaining = \
            config.levels[self.current_level_index].level_max_time

        self.points_per_pacgum = config.points_per_pacgum
        self.points_per_super_pacgum = config.points_per_super_pacgum
        self.points_per_ghost = config.points_per_ghost

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

        # self.player = Player(start_col=1, start_row=1, tile_size=self.tile_w)
    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def add_score(self, points: int) -> None:
        """Increase the score by the given amount of points"""
        self.score += points

    def lose_life(self) -> None:
        """Remove a life when hit"""
        self.lives = max(0, self.lives - 1)

    def update_hud(self):
        """Refresh HUD text objects from current game state."""
        self.score_text.text = f"Score: {self.score}"
        self.lives_text.text = f"Lives: {self.lives}"
        self.level_text.text = f"Level: {self.level}"
        self.time_text.text = f"Time: {int(self.time_remaining)}"

    def on_update(self, delta_time: float):
        # self.player.update_position()
        self.time_remaining = max(0, self.time_remaining - delta_time)
        self.update_hud()

    def on_draw(self):
        """Render the screen."""
        self.clear()

        self.tiles_list.draw()
        self.hud_sprite_list.draw()

        self.score_text.draw()
        self.lives_text.draw()
        self.level_text.draw()
        self.time_text.draw()

    def on_key_press(self, key, key_modifiers):
        """Called whenever a key on the keyboard is pressed."""
        if key == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)
        if key == arcade.key.ESCAPE:
            arcade.close_window()


def run_game(maze: list[list[int]], config: ConfigFile):
    window = GameView(maze, config)
    window.setup()
    arcade.run()
