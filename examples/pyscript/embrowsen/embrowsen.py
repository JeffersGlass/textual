from textual.screen import Screen
from textual.widgets import DirectoryTree, TextLog, Placeholder
from textual.app import App
from textual.containers import Horizontal
from textual.binding import Binding

import sys
IN_BROWSER = 'pyodide' in sys.modules
if IN_BROWSER: from textual.pyscript_app import PyScriptApp

class Home(Screen):
    d = DirectoryTree('/')
    t = TextLog(highlight=True)

    def compose(self):
        yield self.d
        #yield Placeholder(variant="text")
        yield self.t

    def on_mount(self):
        self.set_focus(self.t)
        
    def on_directory_tree_file_selected( self, event: DirectoryTree.FileSelected ) -> None:
        try:
            with open(event.path, 'r') as f:
                self.t.clear()
                self.t.write(f.read())
        except UnicodeDecodeError as err:
            self.t.clear()
            self.t.write("Could not decode unicode from file")

super_class = PyScriptApp if IN_BROWSER else App

class Embrowsen(super_class):
    CSS_PATH = "embrowsen.css"
    SCREENS = {
        "home": Home,
    }
    BINDINGS = [
        Binding( "space", "submit", "", show=False ),
    ]

    def on_mount(self) -> None:
        self.push_screen("home")
        

if not IN_BROWSER:

    if __name__ == "__main__":
        app = Embrowsen()
        app.run()