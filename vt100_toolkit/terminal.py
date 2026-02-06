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
import colorsys
import os
import sys
import termios
import tty

from . import vt100

####################################################################################################

LINESEP = os.linesep

type Int2 = list[int, int]
type Int3 = list[int, int, int]
type RGBColor = list[int, int, int]

####################################################################################################

class Colours(Enum):
    red = '#cc5555',
    green = (0, 200, 0)
    blue = '#0000ff'

class Theme:
    COLOURS = {
        'red': '#cc5555',
        'green': (0, 200, 0),
        'blue': '#0000ff',
    }
    # colours = Colours

    ##############################################

    def foreground(self, name: str) -> str:
        # color = self.colours[name].value
        color = self.COLOURS.get(name, None)
        if color is None:
            raise ValueError(f"Unknown foreground colour {name}")
        if isinstance(color, str):
            if color.startswith('#'):
                rgb = [int(color[_:_+2], 16) for _ in range(1, 6, 2)]
            else:
                raise NotImplementedError
        elif isinstance(color, (tuple, list)):
            rgb = color[:3]
        else:
            raise ValueError(f"unsuported foreground style {name} {color}")
        return vt100.sgr(38, 2, *rgb)

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

    def _read_tty(self, until_chr: str) -> str:
        # It only works if the terminal is set in `cbreak` mode
        # See `query` method
        buffer = ''
        while True:
            buffer += sys.stdin.read(1)
            if buffer[-1] == until_chr:
                break
        if self._debug:
            self._debug_tty_read(buffer)
        return buffer

    ##############################################

    def query(self, command: str, read_callback) -> None:
        # Fixme: use ContextManager see curtsies
        #   https://github.com/thomasballinger/curtsies/blob/master/curtsies/termhelpers.py
        stdin = sys.stdin.fileno()
        # same as
        # stdin = Path('/dev/tty').open('r')
        # save tty attributes
        # https://docs.python.org/3.14/library/tty.html
        # https://docs.python.org/3.14/library/termios.html
        terminal_attribute = termios.tcgetattr(stdin)
        try:
            # TCSANOW means change NOW
            # clears the ECHO and ICANON local mode flags
            # as well as setting the minimum input to 1 byte with no delay
            tty.setcbreak(stdin, termios.TCSANOW)
            self.send(command)
            self._stdout.flush()
            read_callback()
        finally:
            # restore tty attributes
            termios.tcsetattr(stdin, termios.TCSANOW, terminal_attribute)

    ##############################################

    def _debug_tty_read(self, buffer: str) -> None:
        _ = vt100.escape_ansi(buffer)
        print(f"Received from TTY '{_}'")

    @property
    def cursor_position(self) -> list[int, int]:
        position = []

        def read_callback():
            buffer = self._read_tty('R')
            # reading the actual values, but what if a keystroke appears while reading from stdin?
            # As dirty work around, returns None if this fails
            nonlocal position
            try:
                # buffer is \x1b[10;20R
                matches = vt100.REPORT_CURSOR_RE.match(buffer)
                position = [int(_) for _ in matches.groups()]
            except AttributeError:
                position = None

        self.query(vt100.REPORT_CURSOR_POSITION, read_callback)
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

        def read_callback():
            buffer = self._read_tty(vt100.C0ControlCodes.BELL)
            # len(buffer) == 24
            # See cursor_position read_callback
            nonlocal color
            try:
                #              123456789 123456789 123
                # buffer is \x1b]11;rgb:2323/2626/2727\a
                #               ]10;rgb:fcfc/fcfc/fcfc\a
                matches = vt100.REPORT_COLOR_RE.match(buffer)
                color = [int(_[:2], 16) for _ in matches.groups()]
            except AttributeError:
                color = None

        self.query(command, read_callback)
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
