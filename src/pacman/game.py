import arcade
from .maze.maze_builder import build_maze
from .maze.maze_factory import generate_maze
from .models.config import ConfigFile
from .entities.player import Player
from .entities.pacgum import PacgumList
from .entities.ghost import Ghost

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Pac-Man"
MAZE_COLOR = arcade.csscolor.BLACK

HUD_HEIGHT = 60
BORDER_THICKNESS = 1
HUD_BORDER_COLOR = (25, 60, 150)
MAZE_AREA_HEIGHT = WINDOW_HEIGHT - HUD_HEIGHT


class GameView(arcade.View):
    def __init__(self, maze: list[list[int]], config: ConfigFile):

        super().__init__()
        self.game_config = config
        self.background_color = MAZE_COLOR

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
        self.cheat_text = arcade.Text(
            "", 300, HUD_HEIGHT / 2, arcade.color.RED,
            12, anchor_y="center"
        )

        self.current_level_index = 0
        self.score = 0
        self.lives = config.lives

        self.points_per_pacgum = config.points_per_pacgum
        self.points_per_super_pacgum = config.points_per_super_pacgum
        self.points_per_ghost = config.points_per_ghost

        self.cheat_mode = False
        self.invincible = False
        self.ghosts_frozen = False

        self._load_level(maze)

    def _load_level(self, maze: list[list[int]]) -> None:
        """Build everything that depends on the maze of the current level."""
        config = self.game_config
        level = config.levels[self.current_level_index]
        self.level = self.current_level_index + 1
        self.time_remaining = float(level.level_max_time)

        self.tiles_list, self.tile_size, self.offset_y, self.offset_x = \
            build_maze(maze, WINDOW_WIDTH, MAZE_AREA_HEIGHT,
                       height_hud=HUD_HEIGHT)

        self.pacgum_list = PacgumList(config.pacgum,
                                      config.points_per_super_pacgum,
                                      config.points_per_pacgum,
                                      maze)
        self.pacgum_list.init_pacgum(self.tile_size)

        self.player = Player(start_col=3, start_row=3,
                             tile_size=self.tile_size, maze=maze)
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.Sprite(
            "assets/pacman_sprites/pacman_up_closed.png")
        self.player_sprite.width = self.player.size
        self.player_sprite.height = self.player.size
        self.player_list.append(self.player_sprite)

        self.ghost = Ghost(15, 15, self.tile_size, maze)
        self.ghost_list = arcade.SpriteList()
        self.ghost_sprite = arcade.Sprite(
            "assets/ghost_sprites/blinky/sprite-6-1.png")
        self.ghost_sprite.width = self.tile_size * 0.6
        self.ghost_sprite.height = self.tile_size * 0.6
        self.ghost_list.append(self.ghost_sprite)

        self.update_hud()

    def add_score(self, points: int) -> None:
        """Increase the score by the given amount of points"""
        self.score += points

    def lose_life(self) -> None:
        """Remove a life when hit"""
        if self.invincible:
            return
        self.lives = max(0, self.lives - 1)

    def _next_level(self) -> None:
        """Load the next level, or leave the game after the last one."""
        self.current_level_index += 1
        levels = self.game_config.levels

        if self.current_level_index >= len(levels):
            print(f"All levels completed! Final score: {self.score}")
            self._back_to_menu()
            return

        level = levels[self.current_level_index]
        try:
            maze = generate_maze(level.width, level.height)
        except Exception as e:
            print(f"Maze generation failed: {e}")
            self._back_to_menu()
            return
        self._load_level(maze)

    def _back_to_menu(self) -> None:
        """Switch back to the main menu."""
        from .views.menu_view import MenuView
        self.window.show_view(MenuView(self.game_config))

    def update_hud(self):
        """Refresh HUD text objects from current game state."""
        self.score_text.text = f"Score: {self.score}"
        self.lives_text.text = f"Lives: {self.lives}"
        self.level_text.text = f"Level: {self.level}"
        self.time_text.text = f"Time: {int(self.time_remaining)}"

        if self.cheat_mode:
            parts = ["CHEAT"]
            if self.invincible:
                parts.append("INV")
            if self.ghosts_frozen:
                parts.append("FREEZE")
            self.cheat_text.text = " ".join(parts)
        else:
            self.cheat_text.text = ""

    def on_update(self, delta_time: float):
        self.player.update_position()
        self.score += self.pacgum_list.pacgum_eated(self.player)

        if all(p.eated for p in self.pacgum_list.pacgum_list):
            self._next_level()
            return

        self.time_remaining = max(0, self.time_remaining - delta_time)
        if not self.ghosts_frozen:
            self.ghost.get_next_direction(self.player.row_col())
            self.ghost.update_position()
        self.update_hud()

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.tiles_list.draw()

        self.player_sprite.center_x = self.player.center_x + self.offset_x
        self.player_sprite.center_y = self.player.center_y + self.offset_y
        self.ghost_sprite.center_x = self.ghost.center_x + self.offset_x
        self.ghost_sprite.center_y = self.ghost.center_y + self.offset_y

        self.pacgum_list.show_pacgum(self.offset_y, self.offset_x).draw()
        self.player_list.draw()
        self.ghost_list.draw()

        self.hud_sprite_list.draw()
        self.score_text.draw()
        self.lives_text.draw()
        self.level_text.draw()
        self.time_text.draw()
        self.cheat_text.draw()

    def on_key_press(self, key, key_modifiers):
        """Called whenever a key on the keyboard is pressed."""
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.UP:
            self.player.next_direction = (1, 0)
        elif key == arcade.key.DOWN:
            self.player.next_direction = (-1, 0)
        elif key == arcade.key.RIGHT:
            self.player.next_direction = (0, 1)
        elif key == arcade.key.LEFT:
            self.player.next_direction = (0, -1)
        elif key == arcade.key.F1:
            self.cheat_mode = not self.cheat_mode
            if not self.cheat_mode:
                self.invincible = False
                self.ghosts_frozen = False
        elif self.cheat_mode and key == arcade.key.N:
            self._next_level()
        elif self.cheat_mode and key == arcade.key.L:
            self.lives += 1
        elif self.cheat_mode and key == arcade.key.I:
            self.invincible = not self.invincible
        elif self.cheat_mode and key == arcade.key.F:
            self.ghosts_frozen = not self.ghosts_frozen


def run_game(maze: list[list[int]], config: ConfigFile):
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    window.show_view(GameView(maze, config))
    arcade.run()
