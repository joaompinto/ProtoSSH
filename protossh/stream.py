# https://vt100.net/docs/vt102-ug/appendixd.html

import sys
from enum import Enum, auto


class StreamProcessError(Exception):
    pass


class Mode(Enum):
    TEXT = auto()
    ESCAPE = auto()
    MODE = auto()
    PARAMS = auto()


ESC = 0x1B


class TerminalStream:
    def __init__(self):
        self.escape_sequence = ""
        self.title = ""
        self.set_mode(Mode.TEXT)

    def set_mode(self, mode):
        self.mode = mode
        self.mode_func = getattr(self, f"handle_mode_{mode.name}")

    def handle_mode_ESCAPE(self, ch):
        self.escape_sequence += chr(ch)
        if ch in range(0x40, 0x5F):
            self.set_mode(Mode.PARAMS)
        else:
            sys.stdout.write(self.escape_sequence)
            self.set_mode(Mode.TEXT)

    def handle_mode_PARAMS(self, ch):
        if chr(ch) in "?0123456789;":
            self.escape_sequence += chr(ch)
        else:
            self.escape_sequence += chr(ch)
            sys.stdout.write(self.escape_sequence)
            self.set_mode(Mode.TEXT)

    def handle_mode_TEXT(self, ch):
        if ch == ESC:
            self.set_mode(Mode.ESCAPE)
            self.escape_sequence = chr(ESC)
        else:
            sys.stdout.write(chr(ch))
            sys.stdout.flush()

    def feed(self, data):
        self.data = data
        for ch in data:
            #sys.stdout.write(chr(ch))
            #sys.stdout.flush()
            self.mode_func(ch)
