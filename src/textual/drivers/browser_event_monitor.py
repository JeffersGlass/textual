import asyncio
from functools import partial
import sys

from ..events import Key
from ..browser_keys import BROWSER_CHARCODES, BROWSER_KEYCODES

if 'pyodide' not in sys.modules:
    raise OSError('You must be running in a browser to use browserEventMonitor')

from pyodide.ffi import create_proxy

class BrowserEventMonitor():
    """Captures events from an HTML DOM element
    And passes them to the event loop"""

    LOCAL_EVENTS = {
        'click': '_click'
    }

    GLOBAL_EVENTS = {
        'keypress': '_keypress'
    }

    def __init__(self, process_event, target, restricted_keycombos):
        import js
        from pyodide.ffi import to_js
        from pyodide.ffi.wrappers import add_event_listener

        #TODO would be nice to pass in DOM element to constructor
        #self.dom_target = js.document.getElementById("output")
        self.process_event = process_event
        self.target = target
        self.restricted_keycombos = restricted_keycombos
        self.capture_global_keys = True #TODO Add a way to disable this

        for evt in self.LOCAL_EVENTS:
            #print(f"Adding event trigger {evt}  with function name {self.LOCAL_EVENTS[evt]}")
            add_event_listener(self.dom_target, evt, getattr(self, self.LOCAL_EVENTS[evt]))

        for evt in self.GLOBAL_EVENTS:
            #print(f"Adding event trigger {evt}  with function name {self.GLOBAL_EVENTS[evt]}")
            add_event_listener(js.document, evt, getattr(self, self.GLOBAL_EVENTS[evt]))

        js.document.onkeydown = self._global_key_handler
        #for key in captured_restricted_keys:

    def _global_key_handler(self,evt):
        if self.capture_global_keys:
            if evt.keyCode in self.restricted_keycombos:
                evt.preventDefault()
                evt.stopPropagation()

                key, char = self.restricted_keycombos[evt.keyCode]
                event = Key(self.target, key, char)
                self.process_event(event)
        
        #Uncomment to log any keys
        #import js
        #js.console.log(evt)

    def set_global_capture(self, capture: bool):
        self.capture_global_keys = capture

    def _click(self, evt):
        import js
        js.console.log(f"Click {evt}")

    def _keypress(self, evt):
        message = f"_keypress: Key({self.target=}, {evt.key=}, {evt.charCode=})"
        import js
        js.console.log(message)
        #js.console.log(evt)

        if evt.charCode in BROWSER_CHARCODES:
            key, char = BROWSER_CHARCODES[evt.charCode]
        elif evt.keyCode in BROWSER_KEYCODES:
            key, char = BROWSER_KEYCODES[evt.keyCode]
        else:
            key, char = evt.key, evt.key

        event = Key(self.target, key, char)
        self.process_event(event)

