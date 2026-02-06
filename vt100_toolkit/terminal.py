####################################################################################################
#
# Copyright (C) 2026 Fabrice SALVAIRE
# SPDX-License-Identifier: AGPL-3.0-or-later
#
####################################################################################################

"""This module generates ANSI character codes to printing colors to terminals.

See: http://en.wikipedia.org/wiki/ANSI_escape_code

"""

####################################################################################################

from pathlib import Path
import colorsys
import os
import re
import sys
import termios
import tty

from . import ansi

####################################################################################################

LINESEP = os.linesep

type Int2 = list[int, int]
type Int3 = list[int, int, int]
type RGBColor = list[int, int, int]

####################################################################################################

class Terminal:

    DEV_TTY = Path('/dev/tty')

    ##############################################

    def __init__(self, debug: bool = False) -> None:
        # Fixme: size and debug is messed !
        self._debug = bool(debug)
        # self._stdout = open(self.DEV_TTY, mode='w')
        self._stdout = sys.stdout

    ##############################################

    def send(self, sequence: str = '') -> None:
        if self._debug:
            _ = ansi.escape_ansi(sequence)
            print(f"Send ANSI sequence '{_}'")
        self._stdout.write(sequence)

    ##############################################

    def query(self, command: str, read_callback) -> None:
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
        _ = ansi.escape_ansi(buffer)
        print(f"Received from TTY '{_}'")

    @property
    def cursor_position(self) -> list[int, int]:
        position = []

        def read_callback():
            buffer = ''
            while True:
                buffer += sys.stdin.read(1)
                if buffer[-1] == 'R':
                    break
            if self._debug:
                self._debug_tty_read(buffer)
            # reading the actual values, but what if a keystroke appears while reading from stdin?
            # As dirty work around, returns None if this fails
            nonlocal position
            try:
                # buffer is \x1b[10;20R
                matches = re.match(r'^\x1b\[(\d*);(\d*)R', buffer)
                position = [int(_) for _ in matches.groups()]
                # i = buffer.find('[')
                # position = [int(_) for _ in buffer[i+1:-1].split(';')]
            except AttributeError:
                position = None

        self.query(ansi.REPORT_CURSOR_POSITION, read_callback)
        return position

    @property
    def size(self) -> Int2:
        old = self.cursor_position
        self.send(ansi.cursor_position(*[9999]*2))
        size = self.cursor_position
        self.send(ansi.cursor_position(*old))
        return size

    ##############################################

    def _report_color(self, command: str) -> RGBColor:
        color = []

        def read_callback():
            buffer = ''
            while True:
                buffer += sys.stdin.read(1)
                if buffer[-1] == ansi.C0ControlCodes.BELL:
                    break
                # if len(buffer) == 24:
                #     break
            if self._debug:
                self._debug_tty_read(buffer)
            # See cursor_position read_callback
            nonlocal color
            try:
                #              123456789 123456789 123
                # buffer is \x1b]11;rgb:2323/2626/2727\a
                #               ]10;rgb:fcfc/fcfc/fcfc\a
                # print(command[1:], len(buffer), buffer[1:])
                matches = re.match(r'^\x1b\]\d\d;rgb:([a-f0-9]{4})/([a-f0-9]{4})/([a-f0-9]{4})', buffer)
                color = [int(_[:2], 16) for _ in matches.groups()]
                # i = buffer.find(':')
                # color = [int(_[:2], 16) for _ in buffer[i+1:-1].split('/')]
            except AttributeError:
                color = None

        self.query(command, read_callback)
        return color

    @property
    def background_color(self) -> RGBColor:
        return self._report_color(ansi.REPORT_BACKGROUND_COLOR)

    @property
    def foreground_color(self) -> RGBColor:
        return self._report_color(ansi.REPORT_FOREGROUND_COLOR)

    @property
    def is_dark_background(self) -> bool:
        color = colorsys.rgb_to_hls(*self.background_color)
        return color[1] < 128

    ##############################################

    def print(self, message: str = '') -> None:
        self._stdout.write(message + LINESEP)

    ##############################################

    def clear(self) -> None:
        self.send(ansi.clear_screen())
        self.send(ansi.cursor_position())
