import asyncio

from rich.console import Console

from ..driver import Driver
from .browser_event_monitor import BrowserEventMonitor
from ..geometry import Size
from ..events import Event, Resize


class PyScriptDriver(Driver):
    """Powers display and input in PyScript"""

    def __init__(
        self,
        console: "Console",
        target: "MessageTarget",
        *,
        debug: bool = False,
        size: tuple[int, int] | None = None,
    ) -> None:
        super().__init__(console, target, debug=debug, size=size)
        self._target = target
        self.console: Console = console

        #self.exit_event = Event()
        #self._event_thread: Thread | None = None        

    def start_application_mode(self) -> None:
        self._event_monitor = BrowserEventMonitor(self.process_event, self._target)

        size = Size(width = self.console.width, height = self.console.height)
        event = Resize(self._target, size, size)
        asyncio.ensure_future(self._target.post_message(event), loop=asyncio.get_running_loop())

    def disable_input(self) -> None:
        pass

    def stop_application_mode(self) -> None:
        print("Stopping application mode")