from enum import IntEnum
from collections import namedtuple

KeyCombo = namedtuple("KeyCombo", ["key", "char"])

# Maps charcodes from keypress to Terminal keys
BROWSER_CHARCODES = {
    13: KeyCombo(key="enter", char="\r"),
    37: KeyCombo(key="percent_sign", char="%"),
    42: KeyCombo(key="asterisk", char="*"),
    43: KeyCombo(key="plus", char="+"),
    45: KeyCombo(key="minus", char="-"),
    46: KeyCombo(key="full_stop", char="."),
    47: KeyCombo(key="slash", char="/"),
    61: KeyCombo(key="equals_sign", char="="),
    63: KeyCombo(key="slash", char="/"),
}


RESTRICTED_KEYCODES = {
    9: KeyCombo(key="tab", char="\t"),
    191: KeyCombo(key="slash", char="/")
}