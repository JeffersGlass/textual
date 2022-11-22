from textual.pyscript_app import PyScriptApp

from textual.widgets import Header, Footer, Static, Label
from textual import events

class SingleApp(PyScriptApp):
    def compose(self):
        yield Header()
        stripe = Static()
        stripe.styles.height = "1fr"
        stripe.styles.background = "red"
        yield stripe

        text = Static("JEFF", )
        text.styles.content_align = ('center', 'middle')
        yield text

        yield Footer()

    def _on_key(self, event: events.Key) -> None:
        if event.key == 'r':
            self.refresh()