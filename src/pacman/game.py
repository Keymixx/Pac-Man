import arcade
from .maze.maze_builder import draw_maze

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Pac-Man"

class GameView(arcade.Window):
    def __init__(self, maze: list[list[int]]):

        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, maze)
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.maze = maze

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""
        draw_maze(self.maze, WINDOW_WIDTH, WINDOW_HEIGHT)

def run_game(maze: list[list[int]]):
    window = GameView(maze)
    window.setup()
    arcade.run()