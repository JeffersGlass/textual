import asyncio
from functools import partial
import sys

from ..events import Key, MouseDown, MouseUp
from ..browser_keys import BROWSER_CHARCODES, BROWSER_KEYCODES

if 'pyodide' not in sys.modules:
    raise OSError('You must be running in a browser to use browserEventMonitor')

from pyodide.ffi import create_proxy

class BrowserEventMonitor():
    """Captures events from an HTML DOM element
    And passes them to the event loop"""

    MOUSE_EVENTS = {
        'click': '_click',
        'mousedown': '_mousedown',
        'mouseup': '_mouseup'
    }

    GLOBAL_EVENTS = {
        'keypress': '_keypress'
    }

    def __init__(self, process_event, target, restricted_keycombos, dom_target=None):
        import js
        from pyodide.ffi import to_js
        from pyodide.ffi.wrappers import add_event_listener

        #TODO would be nice to pass in DOM element to constructor
        #self.dom_target = js.document.getElementById("output")
        self.process_event = process_event
        self.target = target
        self.restricted_keycombos = restricted_keycombos
        self.capture_global_keys = True #TODO Add a way to disable this
        self.dom_target = dom_target

        for evt in self.MOUSE_EVENTS:
            #print(f"Adding event trigger {evt}  with function name {self.MOUSE_EVENTS[evt]} to {self.dom_target}")
            from pyodide.ffi import create_proxy
            from js import document
            dom_target.parentElement.addEventListener(evt, create_proxy(getattr(self, self.MOUSE_EVENTS[evt])), True)
            #add_event_listener(self.dom_target.parentElement, evt, getattr(self, self.MOUSE_EVENTS[evt]))

        def logit(s):
            js.console.log(s)
        add_event_listener(js.document, 'click', logit)

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
                event = Key(key, char)
                self.process_event(event)
        
        #Uncomment to log any keys
        import js
        js.console.log(evt)

    def set_global_capture(self, capture: bool):
        self.capture_global_keys = capture

    def _click(self, evt):
        import js
        js.console.log(evt)

    def _mousedown(self, evt):
        import js
        js.console.log(evt)

        event = MouseDown(
            x = 0,
            y = 0,
            delta_x = 0,
            delta_y = 0,
            button = evt.button,
            shift = evt.shiftKey,
            meta = evt.metaKey,
            ctrl = evt.ctrlKey,
        )
        self.process_event(event)

    def _mouseup(self, evt):
        import js
        js.console.log(evt)

        event = MouseUp(
            x = 0,
            y = 0,
            delta_x = 0,
            delta_y = 0,
            button = evt.button,
            shift = evt.shiftKey,
            meta = evt.metaKey,
            ctrl = evt.ctrlKey,
        )
        self.process_event(event)

    def _keypress(self, evt):
        message = f"_keypress: Key({self.target=}, {evt.key=}, {evt.charCode=})"
        import js
        js.console.log("_keypress message: ", message)
        #js.console.log(evt)

        if evt.charCode in BROWSER_CHARCODES:
            key, char = BROWSER_CHARCODES[evt.charCode]
        elif evt.keyCode in BROWSER_KEYCODES:
            key, char = BROWSER_KEYCODES[evt.keyCode]
        else:
            key, char = evt.key, evt.key

        #event = Key(self.target, key, char)
        event = Key(key, char)
        self.process_event(event)

