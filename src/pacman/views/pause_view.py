import arcade

from ..game import GameView
from .menu_view import MenuView

OPTIONS = ["Resume the game", "Return to the main menu"]


class PauseView(arcade.View):
    """Pause screen drawn over the frozen game."""

    def __init__(self, game_view: GameView) -> None:
        super().__init__()
        self.game_view = game_view
        self.selected = 0

        w = self.window.width
        h = self.window.height

        self.overlay_list = arcade.SpriteList()
        overlay = arcade.SpriteSolidColor(int(w), int(h), color=(0, 0, 0, 180))
        overlay.center_x = w / 2
        overlay.center_y = h / 2
        self.overlay_list.append(overlay)

        self.title_text = arcade.Text(
            "PAUSED", w / 2, h - 250, arcade.color.YELLOW, 44,
            anchor_x="center", bold=True)
        self.option_texts = [
            arcade.Text(label, w / 2, h - 350 - i * 50, arcade.color.WHITE,
                        22, anchor_x="center")
            for i, label in enumerate(OPTIONS)
        ]
        self.hint_text = arcade.Text(
            "UP / DOWN: choose   |   ENTER: confirm   |   ESC: resume",
            w / 2, 60, arcade.color.GRAY, 13, anchor_x="center")
        self._refresh_options()

    def _refresh_options(self) -> None:
        """Highlight the selected option."""
        for i, text in enumerate(self.option_texts):
            if i == self.selected:
                text.text = f"> {OPTIONS[i]} <"
                text.color = arcade.color.YELLOW
            else:
                text.text = OPTIONS[i]
                text.color = arcade.color.WHITE

    def _resume(self) -> None:
        self.window.show_view(self.game_view)

    def _confirm(self) -> None:
        if self.selected == 0:
            self._resume()
        else:
            self.window.show_view(MenuView(self.game_view.game_config))

    def on_draw(self) -> None:
        self.game_view.on_draw()
        self.overlay_list.draw()
        self.title_text.draw()
        for text in self.option_texts:
            text.draw()
        self.hint_text.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.UP:
            self.selected = (self.selected - 1) % len(OPTIONS)
            self._refresh_options()
        elif symbol == arcade.key.DOWN:
            self.selected = (self.selected + 1) % len(OPTIONS)
            self._refresh_options()
        elif symbol in (arcade.key.ENTER, arcade.key.NUM_ENTER):
            self._confirm()
        elif symbol == arcade.key.ESCAPE:
            self._resume()
