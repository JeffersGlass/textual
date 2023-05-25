import asyncio
from typing import Sequence

from rich.console import Console

from ..driver import Driver
from .xtermjs_monitor import XtermJSMonitor
from ..geometry import Size
from ..events import Event, Resize

from ..app import App

from ..browser_keys import RESTRICTED_KEYCODES
class PyScriptDriver(Driver):
    """Powers display and input in PyScript"""
    captured_restricted_keys: list = {}
    dom_target = None

    def __init__(
        self,
        app: App,
        *,
        debug: bool = False,
        size: tuple[int, int] | None = None,
        
    ) -> None:
        super().__init__(app, debug=debug, size=size)
        self._target = app
        self.console = self._app.console

        #self.exit_event = Event()
        #self._event_thread: Thread | None = None        

    def start_application_mode(self) -> None:
        print("Starting application mode")
        self._event_monitor = XtermJSMonitor(self.process_event, self._target, self.captured_restricted_keys, dom_target=self.dom_target)

        size = Size(width = self._app.console.width, height = self._app.console.height)
        event = Resize(size, size)
        #asyncio.call_later(1, self._target.post_message, event)
        asyncio.ensure_future(self.awaitable_post_message(event), loop=asyncio.get_running_loop())

    async def awaitable_post_message(self, event):
        await asyncio.sleep(0.001)
        self._target.post_message(event)

    def disable_input(self) -> None:
        pass

    def stop_application_mode(self) -> None:
        print("Stopping application mode")
        import traceback
        traceback.print_stack(limit=10)

    @classmethod
    def setRestricted(cls, restricted: Sequence = None):
        if not restricted:
            return
        import js
        for key in restricted:
            if code_list := [code for code, combo in RESTRICTED_KEYCODES.items() if combo.key == key]:
                code = code_list[0]
                js.console.warn(f"Restricting {key}")
                cls.captured_restricted_keys[code] = RESTRICTED_KEYCODES[code]
            else:
                js.console.warn(f"{key} is not a restricted keycode")

    def write(self, data: str):
        self.dom_target.stdout_writeline(data)

    