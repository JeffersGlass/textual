from textual.screen import Screen
from textual.widgets import DirectoryTree,Static

from textual.pyscript_app import PyScriptApp

class Home(Screen):
    def compose(self):
        yield DirectoryTree("/")

class Embrowsen(PyScriptApp):
    CSS_PATH = "embrowsen.css"
    SCREENS = {
        "home": Home,
    }
    BINDINGS = []

    def on_mount(self) -> None:
        self.push_screen("home")