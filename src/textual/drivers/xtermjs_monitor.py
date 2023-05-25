import sys

from ..events import Key, MouseDown, MouseUp
from ..browser_keys import BROWSER_CHARCODES, BROWSER_KEYCODES

if 'pyodide' not in sys.modules:
    raise OSError('You must be running in a browser to use browserEventMonitor')

from pyodide.ffi import create_proxy

class XtermJSMonitor():
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

        #TODO would be nice to pass in DOM element to constructor
        #self.dom_target = js.document.getElementById("output")
        self.process_event = process_event
        self.target = target
        self.restricted_keycombos = restricted_keycombos
        self.capture_global_keys = True #TODO Add a way to disable this
        self.dom_target = dom_target
        
        dom_target.xtermReadyPromise.then(self.attachEvents)

    def dispatchKeyEvent(self, event_object, *args):
        import js
        domEvent = event_object.domEvent
        js.console.log(domEvent)
        js.console.log("charCode", domEvent.charCode)
        js.console.log("keyCode", domEvent.keyCode)

        if self.capture_global_keys:
            if domEvent.keyCode in self.restricted_keycombos:
                domEvent.preventDefault()
                domEvent.stopPropagation()

                key, char = self.restricted_keycombos[domEvent.keyCode]

                js.console.log(f"Handling restricted key {key} {char}")
                event = Key(key, char)
                self.process_event(event)
                return
        
        if domEvent.charCode in BROWSER_CHARCODES:
            js.console.log("Looked up new charcode in BROWSER_CHARCODES")
            key, char = BROWSER_CHARCODES[domEvent.charCode]
        elif domEvent.keyCode in BROWSER_KEYCODES:
            js.console.log("Looked up new keyCode in BROWSER_KEYCODES")
            key, char = BROWSER_KEYCODES[domEvent.keyCode]
        else:
            key, char = domEvent.key, domEvent.key

        js.console.log(key, char)

        new_key_event = Key(key, char)
        self.process_event(new_key_event)

    def attachEvents(self, *args):
        import js
        from pyodide.ffi import to_js
        from pyodide.ffi.wrappers import add_event_listener
        from pyodide.ffi import create_proxy

        self.xterm = self.dom_target.xterm  
        self.xterm.onKey(create_proxy(self.dispatchKeyEvent))
    
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

