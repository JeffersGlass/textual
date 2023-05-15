from js import document
from embrowsen.embrowsen import Embrowsen

Embrowsen(document.querySelector('py-terminal'), restricted=['up', 'down', 'left', 'right', 'enter', 'tab']).run()       