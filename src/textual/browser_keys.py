from enum import IntEnum
from collections import namedtuple

KeyCombo = namedtuple("KeyCombo", ["key", "char"])

# Maps charcodes from keypress to Terminal keys
BROWSER_CHARCODES = {
    13: KeyCombo(key="enter", char="\r"),
    42: KeyCombo(key="asterisk", char="*"),
    43: KeyCombo(key="plus", char="+"),
    45: KeyCombo(key="minus", char="-"),
    46: KeyCombo(key="full_stop", char="."),
    47: KeyCombo(key="slash", char="/"),
    53: KeyCombo(key="percent_sign", char="%"),
    61: KeyCombo(key="equals_sign", char="="),
    63: KeyCombo(key="slash", char="/"),
    
}


BROWSER_KEYCODES = {
}

RESTRICTED_KEYCODES = {
    9: KeyCombo(key="tab", char="\t"),
    37: KeyCombo(key="left", char=""),
    38: KeyCombo(key="up", char=""),
    39: KeyCombo(key="right", char=""),
    40: KeyCombo(key="down", char=""),
    191: KeyCombo(key="slash", char="/")
}