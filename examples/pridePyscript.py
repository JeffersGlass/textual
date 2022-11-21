from textual.pyscript_app import PyScriptApp
from decimal import Decimal

from textual.app import App, ComposeResult
from textual import events
from textual.containers import Container
from textual.css.query import NoMatches
from textual.reactive import var
from textual.widgets import Button, Static

from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.reactive import var
from textual.widgets._label import Label


class PrideApp(PyScriptApp):
    """Displays a pride flag."""

    COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
    label = var("START")

    def watch_label(self, value: str) -> None:
        self.query_one("#label", Static).update(value)

    def compose(self) -> ComposeResult:
        yield Static(id="label")

        for color in self.COLORS:
            stripe = Static()
            stripe.styles.height = "1fr"
            stripe.styles.background = color
            yield stripe
        
        
    def on_click(self):
        self.label += "A"
