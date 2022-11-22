import asyncio
from collections import deque
from io import TextIOBase
import sys
from typing import (
    Iterable
)

import rich
from rich.segment import Segment
from rich.console import RenderableType
import rich.console

from .app import (
    App,
    CSSPathType,
    ReturnType
)
from .drivers.pyscript_driver import PyScriptDriver
from .screen import Screen

rich.console._is_jupyter = lambda : True
rich.console.JUPYTER_DEFAULT_COLUMNS = 80
rich.console.JUPYTER_DEFAULT_LINES = 40

def make_display_function(dom_target):
    def display_pyscript(segments: Iterable[Segment], text: str) -> None:
        """Allow output of raw HTML within pyscript/pyodide"""
        html = rich.jupyter._render_segments(segments)
        dom_target.innerHTML = html       
    return display_pyscript
class _DOMWriter(TextIOBase):
    """A coroutine-runner / file-like to do writes to stdout in the background."""

    def __init__(self, dom_target) -> None:
        self._queue: deque[str | None] = deque()
        self.dom_target = dom_target

    def write(self, text: str) -> None:
        """Write text. Text will be enqueued for writing.

        Args:
            text (str): Text to write to the file.
        """
        sys.__stdout__.write("Writing to DOM")
        sys.__stdout__.flush()
        self._queue.append(text)

    def isatty(self) -> bool:
        """Pretend to be a terminal.

        Returns:
            bool: True if this is a tty.
        """
        return True

    def fileno(self) -> int:
        """Get file handle number.

        Returns:
            int: File number of proxied file.
        """
        return self._file.fileno()

    def flush(self) -> None:
        """Flush the file (a no-op, because flush is done in the thread)."""
        self.dom_target.innerHTML = "".join(self._queue)
        self._queue.clear()
class PyScriptApp(App):
    def __init__(
        self,
        dom_target,
        restricted = None,
        css_path: CSSPathType = None,
        watch_css: bool = False,
    ):
        self.dom_target = dom_target
        self.captured_restricted_keys = restricted

        real_stdout = sys.__stdout__
        sys.__stdout__ = None

        PyScriptDriver.setRestricted(restricted)
        PyScriptDriver.dom_target = self.dom_target
        super().__init__(PyScriptDriver, css_path, watch_css)
        
        sys.__stdout__ = real_stdout

        #TODO: figure out writing in coroutine
        #self.console.file = _DOMWriter(self.dom_target)

        self.console.file = None 
        self.console.width = 80
        self.console.height = 40

        rich.jupyter.display = make_display_function(dom_target = self.dom_target)

    def run(
        self,
        *,
        headless: bool = False,
        size: tuple[int, int] | None = None,
        auto_pilot = None,
    ) -> ReturnType | None:
        """Run the app.

        Args:
            headless (bool, optional): Run in headless mode (no output). Defaults to False.
            size (tuple[int, int] | None, optional): Force terminal size to `(WIDTH, HEIGHT)`,
                or None to auto-detect. Defaults to None.
            auto_pilot (AutopilotCallbackType): An auto pilot coroutine.

        Returns:
            ReturnType | None: App return value.
        """

        async def run_app() -> None:
            """Run the app."""
            await self.run_async(
                headless=headless,
                size=size,
                auto_pilot=auto_pilot,
            )

        asyncio.create_task(run_app())
        return self.return_value

    def _display(self, screen: Screen, renderable: RenderableType | None) -> None:
        super()._display(screen, renderable)
        self.refresh()