import os
import sys
from enum import Enum, auto


class INPUT(Enum):
    TEXT = auto()
    ESCAPE = auto()
    ESCAPE_FUNC = auto()
    ESCAPE_PARAMS = auto()


ESC = 0x1b


# https://vt100.net/docs/vt102-ug/appendixd.html
class TerminalStream:
    def __init__(self):
        self.escape_sequence = ""
        self.set_mode(INPUT.TEXT)

    def _handle_ESCAPE(self, ch):
        self.escape_sequence += chr(ch)
        if ch in range(0x40, 0x5F):
            self.set_mode(INPUT.ESCAPE_PARAMS)
        else:
            sys.stdout.write(self.escape_sequence)
            self.set_mode(INPUT.TEXT)

    def _handle_ESCAPE_PARAMS(self, ch):
        self.escape_sequence += chr(ch)
        if not chr(ch) in "?0123456789;":   # End of ESC parameters
            sys.stdout.write(self.escape_sequence)
            self.set_mode(INPUT.TEXT)

    def _handle_TEXT(self, ch):
        if ch == ESC:
            self.set_mode(INPUT.ESCAPE)
            self.escape_sequence = chr(ESC)
        else:
            sys.stdout.write(chr(ch))
            sys.stdout.flush()

    def set_mode(self, mode):
        self.mode = mode
        self.mode_func = getattr(self, f"_handle_{mode.name}")

    def feed(self, data):
        self.data = data
        for ch in data:
            self.mode_func(ch)


def set_ansi_mode():
    if os.name == "nt":  # Only if we are running on Windows
        from ctypes import windll

        k = windll.kernel32
        k.SetConsoleMode(k.GetStdHandle(-11), 7)
