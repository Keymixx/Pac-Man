import arcade

from ..highscore_loader import add_highscore, load_highscores, save_highscores
from ..models.config import ConfigFile
from .menu_view import MenuView

MAX_NAME_LENGTH = 10


class EndView(arcade.View):
    """End screen (game over or victory) with name entry for the highscores."""
    def __init__(self, config: ConfigFile, score: int, won: bool,
                 reason: str) -> None:
        super().__init__()
        self.game_config = config
        self.score = score
        self.name = ""
        self.background_color = arcade.color.BLACK

        w = self.window.width
        h = self.window.height

        title = "CONGRATULATIONS!" if won else "GAME OVER"
        title_color = arcade.color.YELLOW if won else arcade.color.RED

        self.title_text = arcade.Text(
            title, w / 2, h - 180, title_color, 44,
            anchor_x="center", bold=True)
        self.reason_text = arcade.Text(
            reason, w / 2, h - 240, arcade.color.GRAY, 16,
            anchor_x="center")
        self.score_text = arcade.Text(
            f"Final score: {score}", w / 2, h - 320, arcade.color.WHITE, 24,
            anchor_x="center")
        self.prompt_text = arcade.Text(
            "Enter your name:", w / 2, h - 400, arcade.color.WHITE, 16,
            anchor_x="center")
        self.name_text = arcade.Text(
            "_", w / 2, h - 450, arcade.color.YELLOW, 28,
            anchor_x="center", bold=True)
        self.error_text = arcade.Text(
            "", w / 2, h - 510, arcade.color.RED, 14, anchor_x="center")
        self.hint_text = arcade.Text(
            "ENTER: save   |   ESC: skip", w / 2, 60, arcade.color.GRAY, 14,
            anchor_x="center")

    def _refresh_name(self) -> None:
        """Show the typed name followed by a cursor."""
        self.name_text.text = self.name + "_"

    def _go_to_menu(self) -> None:
        self.window.show_view(MenuView(self.game_config))

    def _save_and_leave(self) -> None:
        """Save the score under the typed name, then go back to the menu."""
        name = self.name.strip()
        if not name:
            self.error_text.text = "Type at least one letter or digit."
            return

        path = self.game_config.highscore_filename
        try:
            updated = add_highscore(load_highscores(path), name, self.score)
        except ValueError:
            self.error_text.text = "Invalid name."
            return

        if not save_highscores(path, updated):
            self.error_text.text = "Could not save (terminal). ESC to skip."
            return
        self._go_to_menu()

    def on_text(self, text: str) -> None:
        """Receive the characters typed by the player."""
        for char in text:
            if (len(self.name) < MAX_NAME_LENGTH and char.isascii()
                    and (char.isalnum() or char == " ")):
                self.name += char
        self._refresh_name()
        self.error_text.text = ""

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.BACKSPACE:
            self.name = self.name[:-1]
            self._refresh_name()
        elif symbol in (arcade.key.ENTER, arcade.key.NUM_ENTER):
            self._save_and_leave()
        elif symbol == arcade.key.ESCAPE:
            self._go_to_menu()

    def on_draw(self) -> None:
        self.clear()
        self.title_text.draw()
        self.reason_text.draw()
        self.score_text.draw()
        self.prompt_text.draw()
        self.name_text.draw()
        self.error_text.draw()
        self.hint_text.draw()
