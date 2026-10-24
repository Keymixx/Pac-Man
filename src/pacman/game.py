import arcade
from .maze.maze_builder import build_maze
from .maze.maze_factory import generate_maze
from .models.config import ConfigFile
from .entities.player import Player
from .entities.pacgum import PacgumList
from .entities.ghost import Ghost
from time import sleep

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Pac-Man"
MAZE_COLOR = arcade.csscolor.BLACK

HUD_HEIGHT = 60
BORDER_THICKNESS = 1
HUD_BORDER_COLOR = (25, 60, 150)
MAZE_AREA_HEIGHT = WINDOW_HEIGHT - HUD_HEIGHT
RESPAWN_TIME = 10
FREEZE_TIME = 2


class GameView(arcade.View):
    def __init__(self, maze: list[list[int]], config: ConfigFile):

        super().__init__()

        self.player_alive = True
        self.textures_player = {"up": [], "down": [], "left": [], "right": []}
        direction = ["up", "down", "left", "right"]

        for d in direction:
            for i in range(3):
                texture = arcade.load_texture(f"assets/pacman_sprites/{d}/pacman_{d}_{i}.png")
                self.textures_player[d].append(texture)

        self.ghost_textures = {"blinky": {}, "pinky": {}, "inky": {}, "clyde": {}}
        direction = ["up", "down", "left", "right", "afraid"]

        for key in self.ghost_textures.keys():
            for d in direction:
                self.ghost_textures[key][d] = []
                for i in range(3):
                    texture = arcade.load_texture(f"assets/ghost_sprites/{key}/{d}{i}.png")
                    self.ghost_textures[key][d].append(texture)

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

        self.is_retry = False

        self._load_level(maze)


    def _load_level(self, maze: list[list[int]]) -> None:
        """Build everything that depends on the maze of the current level."""
        height = len(maze)
        width = len(maze[0])
        config = self.game_config
        level = config.levels[self.current_level_index]
        self.maze = maze
        self.level = self.current_level_index + 1
        self.time_remaining = float(level.level_max_time)

        self.tiles_list, self.tile_size, self.offset_y, self.offset_x = \
            build_maze(maze, WINDOW_WIDTH, MAZE_AREA_HEIGHT,
                       height_hud=HUD_HEIGHT)

        if not self.is_retry:
            self.pacgum_list = PacgumList(config.pacgum,
                                          config.points_per_super_pacgum,
                                          config.points_per_pacgum,
                                          maze)
            self.pacgum_list.init_pacgum(self.tile_size)

        self.player = Player(start_col=3, start_row=3,
                             tile_size=self.tile_size, maze=maze,
                             textures=self.textures_player)
        self.player_sprite = arcade.Sprite()
        self.player_sprite.texture = self.player.actual_texture
        self.player_sprite.width = self.player.size
        self.player_sprite.height = self.player.size
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        ghost_configs = [
            {"col": 0, "row": 0, "name": "blinky"},
            {"col": width - 1, "row": 0, "name": "pinky"},
            {"col": 0, "row": height - 1, "name": "inky"},
            {"col": width - 1, "row": height - 1, "name": "clyde"}
        ]
        self.ghosts = []
        self.ghost_list = arcade.SpriteList()

        for config in ghost_configs:
            ghost = Ghost(config["col"], config["row"], self.tile_size, maze, self.ghost_textures[config["name"]])
            self.ghosts.append(ghost)

            ghost_sprite = arcade.Sprite()
            ghost_sprite.texture = ghost.actual_texture
            ghost_sprite.width = self.tile_size * 0.6
            ghost_sprite.height = self.tile_size * 0.6
            self.ghost_list.append(ghost_sprite)

        self.super_timer = 0.0
        self.freeze_timer = 0.0
        self.respawn_ghost_timer = 0.0

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
        self.is_retry = False
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
        if self.freeze_timer > 0:
            self.freeze_timer -= delta_time
            if self.freeze_timer <= 0:
                self.freeze_timer = 0
                if not self.player_alive:
                    self.is_retry = True
                    self.player_alive = True
                    self._load_level(self.maze)
            return

        if self.player_alive:
            self.player.update_position()
            self.player.update_animation(delta_time)

        # MISE À JOUR DES 4 FANTÔMES
        for ghost in self.ghosts:
            ghost.update_animation(delta_time)

            ghost.super_timer = self.super_timer

            if ghost.respawn_timer > 0:
                ghost.respawn_timer -= delta_time
                if ghost.respawn_timer <= 0:
                    ghost.respawn_timer = 0
                    ghost.is_eated = False

            if not self.ghosts_frozen and self.player_alive:
                ghost.get_next_direction(self.player.row_col())
                ghost.update_position()

        # GESTION DES PACGUMS
        if self.player_alive:
            earned_point = self.pacgum_list.pacgum_eated(self.player)
            if earned_point > 0:
                self.score += earned_point
                if self.player.super:
                    self.super_timer = 8.0
                    self.player.super = False
                    for ghost in self.ghosts:
                        if not ghost.is_eated:
                            ghost.super = True

        # DÉCOMPTE DU SUPER TIMER
        if self.super_timer > 0:
            self.super_timer -= delta_time
            if self.super_timer <= 0:
                self.super_timer = 0.0
                for ghost in self.ghosts:
                    ghost.super = False

        # VERIF SI FIN DE NIVEAU
        if all(p.eated for p in self.pacgum_list.pacgum_list):
            self._next_level()
            return

        # DÉCOMPTE DU TEMPS
        self.time_remaining = max(0, self.time_remaining - delta_time)

        # GESTION DES COLLISIONS
        if self.player_alive and not self.invincible:
            for ghost in self.ghosts:
                if ghost.row_col() == self.player.row_col():
                    if ghost.super and not ghost.is_eated:
                        # Pac-man mange fantome
                        ghost.is_eated = True
                        ghost.super = False
                        self.score += self.points_per_ghost
                        self.freeze_timer = 0.5
                        ghost.respawn_timer = RESPAWN_TIME
                    elif not ghost.is_eated:
                        # Fantome mange Pac-man
                        self.lose_life()
                        self.player_alive = False
                        self.freeze_timer = 2.0
                    break

        self.update_hud()

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.tiles_list.draw()

        self.player_sprite.texture = self.player.actual_texture

        self.player_sprite.center_x = self.player.center_x + self.offset_x
        self.player_sprite.center_y = self.player.center_y + self.offset_y
        for i, ghost in enumerate(self.ghosts):
            self.ghost_list[i].texture = ghost.actual_texture
            self.ghost_list[i].center_x = ghost.center_x + self.offset_x
            self.ghost_list[i].center_y = ghost.center_y + self.offset_y


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
