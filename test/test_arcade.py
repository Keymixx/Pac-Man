
import arcade
from test_maze_builder import build_maze


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 2.5

class Player:
    def __init__(self):
        self.texture = arcade.Sprite("assets/pacman_sprites/pacman_down_closed.png")

class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.maze, self.tile_width, self.tile_height = build_maze([[9, 1, 1, 3, 9, 1, 3, 9, 1, 1, 1, 1, 3, 9, 1, 3, 9, 1, 1, 5, 3, 9, 1, 5, 3], [8, 6, 8, 4, 0, 6, 12, 2, 10, 8, 6, 10, 8, 2, 10, 8, 4, 2, 8, 3, 12, 4, 6, 9, 2], [8, 1, 6, 9, 0, 1, 3, 10, 8, 4, 3, 8, 4, 4, 2, 12, 5, 0, 2, 12, 5, 5, 5, 4, 2], [8, 4, 5, 6, 10, 8, 0, 2, 12, 1, 4, 4, 1, 3, 8, 5, 3, 8, 4, 5, 3, 9, 3, 9, 2], [12, 5, 3, 9, 6, 12, 0, 4, 1, 4, 1, 3, 10, 8, 4, 5, 6, 10, 9, 5, 4, 2, 10, 8, 6], [9, 3, 10, 8, 5, 3, 10, 9, 6, 9, 6, 8, 6, 8, 1, 1, 1, 2, 8, 1, 1, 4, 2, 8, 3], [8, 2, 10, 10, 9, 2, 10, 10, 9, 6, 9, 6, 9, 4, 2, 8, 6, 10, 12, 2, 8, 5, 6, 8, 2], [10, 8, 4, 2, 10, 12, 0, 6, 12, 5, 0, 1, 6, 9, 4, 2, 9, 0, 3, 10, 8, 5, 1, 6, 10], [8, 2, 9, 2, 8, 3, 12, 3, 9, 3, 10, 10, 9, 2, 9, 4, 0, 2, 10, 10, 8, 3, 10, 9, 2], [8, 6, 12, 2, 10, 10, 9, 4, 6, 12, 4, 4, 4, 4, 4, 5, 2, 12, 0, 4, 6, 10, 12, 4, 2], [10, 9, 1, 6, 10, 10, 8, 1, 3, 15, 9, 1, 3, 15, 15, 15, 8, 3, 8, 1, 3, 12, 5, 3, 10], [8, 6, 8, 5, 4, 4, 4, 4, 2, 15, 12, 6, 8, 5, 7, 15, 10, 10, 12, 2, 12, 5, 1, 4, 2], [12, 3, 8, 1, 5, 1, 1, 1, 6, 15, 15, 15, 10, 15, 15, 15, 10, 8, 3, 8, 1, 5, 2, 9, 2], [9, 0, 2, 10, 9, 0, 2, 8, 5, 1, 3, 15, 10, 15, 13, 5, 0, 4, 6, 10, 8, 5, 2, 10, 10], [8, 4, 0, 6, 12, 4, 2, 10, 9, 2, 10, 15, 10, 15, 15, 15, 10, 9, 5, 6, 8, 1, 4, 2, 10], [12, 5, 4, 5, 5, 3, 8, 2, 10, 8, 4, 5, 0, 5, 3, 9, 0, 4, 5, 1, 6, 8, 1, 6, 10], [9, 3, 9, 5, 3, 8, 4, 2, 10, 8, 3, 9, 4, 3, 8, 4, 6, 9, 5, 0, 3, 10, 8, 5, 6], [8, 4, 6, 9, 6, 10, 9, 6, 8, 0, 2, 10, 9, 6, 10, 9, 1, 6, 9, 2, 12, 6, 12, 1, 3], [12, 1, 1, 2, 9, 2, 8, 5, 2, 10, 10, 10, 10, 9, 6, 12, 4, 3, 12, 4, 5, 5, 5, 4, 6], [9, 6, 12, 4, 6, 8, 0, 1, 4, 2, 8, 2, 8, 6, 9, 1, 5, 4, 1, 1, 3, 9, 1, 1, 3], [8, 5, 1, 5, 5, 6, 10, 8, 3, 12, 6, 8, 4, 1, 2, 8, 5, 1, 6, 10, 10, 10, 10, 8, 2], [12, 5, 4, 1, 5, 3, 10, 8, 4, 1, 1, 2, 9, 2, 8, 2, 9, 4, 1, 6, 10, 10, 8, 4, 2], [9, 5, 5, 2, 9, 2, 12, 0, 1, 4, 4, 2, 12, 4, 2, 10, 8, 5, 2, 9, 2, 12, 6, 9, 6], [8, 5, 3, 8, 2, 8, 3, 10, 8, 1, 3, 8, 1, 1, 2, 12, 4, 1, 2, 8, 2, 9, 3, 12, 3], [12, 5, 4, 4, 4, 6, 12, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 6, 12, 4, 4, 6, 12, 5, 6]], WINDOW_WIDTH, WINDOW_HEIGHT)

        self.player = Player()# Variable to hold our texture for our player
        self.player_texture = self.player.texture


        self.player_sprite = arcade.Sprite("assets/pacman_sprites/pacman_down_closed.png")
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_sprite.width = self.tile_width * 0.65
        self.player_sprite.height = self.tile_height * 0.65


        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)


        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", scale=TILE_SCALING
            )
            wall.position = coordinate
            self.wall_list.append(wall)

        # Create a Simple Physics Engine, this will handle moving our
        # player as well as collisions between the player sprite and
        # whatever SpriteList we specify for the walls.
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.wall_list
        )

        self.background_color = arcade.csscolor.BLACK
        
        


    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        self.player_list.draw()
        self.maze.draw()
        

    def on_update(self, delta_time):
        """Movement and Game Logic"""

        # Move the player using our physics engine
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_y = 0
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_y = 0
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released."""


def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()