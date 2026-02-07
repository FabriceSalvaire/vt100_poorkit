####################################################################################################
#
# vt100_toolkit — A VT100 library
# Copyright (C) 2026 Fabrice SALVAIRE
# SPDX-License-Identifier: AGPL-3.0-or-later
#
####################################################################################################

"""This module implements Terminal IO, i.e. all the UNIX TTY intrinsics.

"""

####################################################################################################

from typing import Callable, Self
import termios
import tty
import sys

from . import vt100

####################################################################################################

class TerminalInput:

    # See also
    #   https://github.com/thomasballinger/curtsies/blob/master/curtsies/termhelpers.py

    ##############################################

    def __init__(self, debug: bool = False) -> None:
        self._debug = bool(debug)

    ##############################################

    def __enter__(self) -> Self:
        self._stdin = sys.stdin
        self._fileno = self._stdin.fileno()
        # same as
        # stdin = Path('/dev/tty').open('r')
        # save tty attributes
        # https://docs.python.org/3.14/library/tty.html
        # https://docs.python.org/3.14/library/termios.html
        self._terminal_attribute = termios.tcgetattr(self._fileno)
        # TCSANOW means change NOW
        # clears the ECHO and ICANON local mode flags
        # as well as setting the minimum input to 1 byte with no delay
        tty.setcbreak(self._fileno, termios.TCSANOW)
        return self

    ##############################################

    def __exit__(self, type, value, traceback) -> None:
        # restore tty attributes
        termios.tcsetattr(self._fileno, termios.TCSANOW, self._terminal_attribute)

    ##############################################

    def _debug_read(self, buffer: str) -> None:
        _ = vt100.escape_ansi(buffer)
        print(f"Received from TTY '{_}'")

    ##############################################

    def read(self, until: str) -> str:
        # It only works if the terminal is set in `cbreak` mode
        # See `query` method
        buffer = ''
        while True:
            buffer += self._stdin.read(1)
            if buffer[-1] == until:
                break
        if self._debug:
            self._debug_read(buffer)
        return buffer
