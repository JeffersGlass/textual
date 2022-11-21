import asyncio
from functools import partial
import sys

from ..events import Key

if 'pyodide' not in sys.modules:
    raise OSError('You must be running in a browser to use browserEventMonitor')

class BrowserEventMonitor():
    """Captures events from an HTML DOM element
    And passes them to the event loop"""

    """ ENABLED_EVENTS = {
        'keydown', 
        'keyup',
        'keypress',
        'click',
        'dblclick',
        'mousedown',
        'mouseup'
    } """

    LOCAL_EVENTS = {
        #'click': '_click'
    }

    GLOBAL_EVENTS = {
        'keypress': '_keypress'
    }

    def __init__(self, process_event, target):
        import js
        from pyodide.ffi import to_js
        from pyodide.ffi.wrappers import add_event_listener

        #TODO would be nice to pass in DOM element to constructor
        #self.dom_target = js.document.getElementById("output")
        self.process_event = process_event
        self.target = target

        for evt in self.LOCAL_EVENTS:
            #print(f"Adding event trigger {evt}  with function name {self.LOCAL_EVENTS[evt]}")
            add_event_listener(self.dom_target, evt, getattr(self, self.LOCAL_EVENTS[evt]))

        for evt in self.GLOBAL_EVENTS:
            #print(f"Adding event trigger {evt}  with function name {self.GLOBAL_EVENTS[evt]}")
            add_event_listener(js.document, evt, getattr(self, self.GLOBAL_EVENTS[evt]))
            
    def _click(self, evt):
        import js
        js.console.log(f"Click {evt}")

    def _keypress(self, evt):
        import js
        js.console.log(f"_keypress: Key({self.target}, {evt.key}, {evt.key})")
        event = Key(self.target, evt.key, evt.key)
        self.process_event(event)

