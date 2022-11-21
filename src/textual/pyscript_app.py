import asyncio
from queue import Queue
import sys
from typing import (
    Type,
    Iterable
)

import rich
from rich.segment import Segment
from rich.console import Console
import rich.console

rich.console._is_jupyter = lambda : True
rich.console.JUPYTER_DEFAULT_COLUMNS = 80
rich.console.JUPYTER_DEFAULT_LINES = 40

def display_pyscript(segments: Iterable[Segment], text: str) -> None:
    """Allow output of raw HTML within pyscript/pyodide"""
    html = rich.jupyter._render_segments(segments)
    import js
    js.document.getElementById("output").innerHTML = html

    #sys.__stdout__.write(html)
    #_pyscript_display("HELLO!", target="output")
    #display(html, target="output")
    

#patch jupyter display method to write processed HTML to stdout
rich.jupyter.display = display_pyscript 

from .app import (
    App,
    CSSPathType,
    ReturnType
)

from .drivers.pyscript_driver import PyScriptDriver

MAX_QUEUED_WRITES: int = 30

class _WriterCoroutine():
    """A coroutine-runner / file-like to do writes to stdout in the background."""

    def __init__(self) -> None:
        self._queue: Queue[str | None] = Queue(MAX_QUEUED_WRITES)
        self._file = sys.__stdout__

    def write(self, text: str) -> None:
        """Write text. Text will be enqueued for writing.

        Args:
            text (str): Text to write to the file.
        """
        self._queue.put(text)

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
        return

    def start(self) -> None:
        self.run()

    def run(self) -> None:
        """Run the thread."""
        write = self._file.write
        flush = self._file.flush
        get = self._queue.get
        qsize = self._queue.qsize
        # Read from the queue, write to the file.
        # Flush when there is a break.
        async def coro():
            while True:
                text: str | None = get()
                empty = qsize() == 0
                if text is None:
                    break
                write(text)
                if empty:
                    flush()
                await asyncio.sleep(1)
        asyncio.ensure_future(coro())

    def stop(self) -> None:
        """Stop the thread, and block until it finished."""
        self._queue.put(None)
        if self._task: self._task.cancel()

class PyScriptApp(App):
    def __init__(
        self,
        css_path: CSSPathType = None,
        watch_css: bool = False,
    ):
        

        real_stdout = sys.__stdout__
        sys.__stdout__ = None
        super().__init__(PyScriptDriver, css_path, watch_css)
        #super().__init__(LinuxDriver, css_path, watch_css)
        sys.__stdout__ = real_stdout

        #TODO: figure out writing in coroutine
        #self._writer_coro = _WriterCoroutine()
        #self._writer_coro.start()
        #self.console.file = self._writer_coro

        self.console.file = sys.__stdout__

        #TODO figure out HTML
        #self.console.is_jupyter = True

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

# Per pyodide docs, determine if we're running inside pyodide at Runtime
#def is_pyodide() -> bool:
#    return "pyodide" in sys.modules

#rich.console._is_jupyter = is_pyodide

""" def display_pyscript(segments: Iterable[Segment], text: str) -> None:
    #Allow output of raw HTML within pyscript/pyodide
    html = rich.jupyter._render_segments(segments)
    print(html)
    import js
    js.console.log("About to write")
    display(HTML(html), target="output") """

#rich.jupyter.display = display_pyscript