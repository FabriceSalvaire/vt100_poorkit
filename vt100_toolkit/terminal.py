####################################################################################################
#
# vt100_toolkit — A VT100 library
# Copyright (C) 2026 Fabrice SALVAIRE
# SPDX-License-Identifier: AGPL-3.0-or-later
#
####################################################################################################

"""This module generates ANSI character codes to printing colors to terminals.

See: http://en.wikipedia.org/wiki/ANSI_escape_code

"""

# See also
#   prompt_toolkit/input/vt100.py
#   prompt_toolkit/input/vt100_parser.py
#   prompt_toolkit/output/vt100.py
#   prompt_toolkit/output/flush_stdout.py

####################################################################################################

from enum import Enum
from pathlib import Path
import colorsys   # rgb_to_hls hls_to_rgb rgb_to_hsv hsv_to_rgb
import math
import os
import sys

from .types import Int2, RGBColor
from . import vt100
from . import vt100_io

####################################################################################################

LINESEP = os.linesep

####################################################################################################

def darken(color: RGBColor, amount: float) -> RGBColor:
    h, s, v = colorsys.rgb_to_hsv(*color)
    v = v * amount
    v = min(max(math.ceil(v), 0), 255)
    return [int(_) for _ in colorsys.hsv_to_rgb(h, s, v)]

####################################################################################################

class Colors(Enum):
    red = '#cc5555'
    green = 0, 200, 0
    blue = '#0000ff'
    blue_light = darken((100, 100, 255), .8)

####################################################################################################

class Theme:
    COLORS = Colors

    ##############################################

    def color(self, name: str) -> RGBColor:
        try:
            color = self.COLORS[name].value
        except KeyError:
            raise ValueError(f"Unknown color {name}")
        if isinstance(color, str):
            if color.startswith('#'):
                return [int(color[_:_+2], 16) for _ in range(1, 6, 2)]
            else:
                raise NotImplementedError
        elif isinstance(color, (tuple, list)):
            return color[:3]
        else:
            raise ValueError(f"unsuported color {name} {color}")

    ##############################################

    def foreground(self, name: str) -> str:
        rgb = self.color(name)
        return vt100.foreground(rgb=rgb)

####################################################################################################

class Terminal:

    DEV_TTY = Path('/dev/tty')

    ESCAPING = [
        ('<', '&lt;'),
        ('>', '&gt;'),
    ]

    ##############################################

    def __init__(self, theme: Theme = None, debug: bool = False) -> None:
        # Fixme: size and debug is messed !
        if theme is None:
            theme = Theme
        self._theme = theme()
        self._debug = bool(debug)
        # self._stdout = open(self.DEV_TTY, mode='w')
        self._stdout = sys.stdout

    ##############################################

    def send(self, sequence: str = '') -> None:
        if self._debug:
            _ = vt100.escape_ansi(sequence)
            print(f"Send ANSI sequence '{_}'")
        self._stdout.write(sequence)
        # self._stdout.flush()

    ##############################################

    def query(self, command: str, read_callback) -> None:
        with vt100_io.TerminalInput(debug=self._debug) as stdin:
            self.send(command)
            self._stdout.flush()
            read_callback(stdin)

    ##############################################

    @property
    def cursor_position(self) -> list[int, int]:
        position = []

        def callback(stdin):
            nonlocal position
            position = vt100.cursor_callback(stdin)

        self.query(vt100.REPORT_CURSOR_POSITION, callback)
        return position

    @property
    def size(self) -> Int2:
        size = os.get_terminal_size(self._stdout.fileno())
        return size.lines, size.columns
        # This code works
        # old = self.cursor_position
        # move cursor to an extreme position that will be clipped to the terminal size
        # self.send(vt100.cursor_position(*[9999]*2))
        # size = self.cursor_position
        # self.send(vt100.cursor_position(*old))
        # return size

    ##############################################

    def _report_color(self, command: str) -> RGBColor:
        color = []

        def callback(stdin):
            nonlocal color
            color = vt100.color_callback(stdin)

        self.query(command, callback)
        return color

    @property
    def background_color(self) -> RGBColor:
        return self._report_color(vt100.REPORT_BACKGROUND_COLOR)

    @property
    def foreground_color(self) -> RGBColor:
        return self._report_color(vt100.REPORT_FOREGROUND_COLOR)

    @property
    def is_dark_background(self) -> bool:
        color = colorsys.rgb_to_hls(*self.background_color)
        return color[1] < 128

    ##############################################

    def clear(self) -> None:
        self.send(vt100.clear_screen())
        self.send(vt100.cursor_position())

    ##############################################

    @classmethod
    def escape(cls, text: str) -> str:
        for a, b in cls.ESCAPING:
            text = text.replace(a, b)
        return text

    @classmethod
    def unescape(cls, text: str) -> str:
        for a, b in cls.ESCAPING:
            text = text.replace(b, a)
        return text

    ##############################################

    def style(self, name: str) -> str:
        return self._theme.foreground(name)

    ##############################################

    def _colorize(self, text: str, escaped: bool = False) -> str:
        raw = ''
        start = 0
        css_stack = []
        while True:
            i = text.find('<', start)
            if i == -1:
                raw += text[start:]
                break
            else:
                raw += text[start:i]
                j = text.find('>', i)
                if j == -1:
                    raise ValueError(f"missing '>' in '{text} @{start}`")
                color = text[i+1:j]
                if color.startswith('/'):
                    # Fixme: complete
                    css_stack.pop()
                    if not css_stack:
                        raw += vt100.SGR_RESET
                    # else:
                else:
                    css_stack.append(color)
                    raw += self.style(color)
                start = j + 1
        if escaped:
            raw = self.unescape(raw)
        return raw

    ##############################################

    def print(self, text: str = '') -> None:
        if self._debug:
            print(vt100.escape_ansi(text))
        self._stdout.write(text + LINESEP)

    def printc(self, text: str = '', escaped: bool = False) -> None:
        _ = self._colorize(text, escaped)
        if self._debug:
            print(vt100.escape_ansi(_))
        self._stdout.write(_ + LINESEP)
