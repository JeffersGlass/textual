from textual.pyscript_app import PyScriptApp

from textual.app import  ComposeResult
from textual.reactive import var
from textual.widgets import Static, Header, Footer
class PrideApp(PyScriptApp):
    """Displays da pride flag."""

    COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header()

        for color in self.COLORS:
            stripe = Static()
            stripe.styles.height = "1fr"
            stripe.styles.background = color
            yield stripe

        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
