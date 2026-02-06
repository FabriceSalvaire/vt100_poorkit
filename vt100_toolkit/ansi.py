####################################################################################################
#
# Copyright (C) 2026 Fabrice SALVAIRE
# SPDX-License-Identifier: AGPL-3.0-or-later
#
####################################################################################################

"""This module implements ANSI escape sequences.

See:
- https://en.wikipedia.org/wiki/ANSI_escape_code
- https://en.wikipedia.org/wiki/Windows_Terminal
- ECMA-48
- ISO/IEC 6429 Information technology — Control functions for coded character sets

"""

####################################################################################################
#
# https://en.wikipedia.org/wiki/ANSI_escape_code
# https://cdn.standards.iteh.ai/samples/12782/9d92ccb5b6694d6abcb9bbe7fa6c21d6/ISO-IEC-6429-1992.pdf
#
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
#
#
# Control Sequence Introducer (CSI) = ESC+[ = \x1B] = \x9B
#
# SGR - Select Graphic Rendition
#   CSI n [;k] m
#   Sets SGR parameters, including text color. After CSI can be zero
#   or more parameters separated with ';'. With no parameters, CSI m is
#   treated as CSI 0 m (reset / normal), which is typical of most of
#   the ANSI escape sequences.
#
# SGR (Select Graphic Rendition)
# parameters Code | Effect | Note
# 0       Reset / Normal    | all attributes off
# 1       Bright (increased intensity) or Bold
# 2       Faint (decreased intensity)    | not widely supported
# 3       Italic: on    | not widely supported. Sometimes treated as inverse.
# 4       Underline: Single
# 5       Blink: Slow    | less than 150 per minute
# 6       Blink: Rapid    | MS-DOS ANSI.SYS; 150 per minute or more; not widely supported
# 7       Image: Negative    | inverse or reverse; swap foreground and background
# 8       Conceal    | not widely supported
# 9       Crossed-out    | Characters legible, but marked for deletion. Not widely supported.
# 10      Primary(default) font
# 11-19   n-th alternate font    | Select the n-th alternate font. 14 being the fourth alternate font, up to 19 being the 9th alternate font.
# 20      Fraktur    | hardly ever supported
# 21      Bright/Bold: off or Underline: Double    | bold off not widely supported, double underline hardly ever
# 22      Normal color or intensity    | neither bright, bold nor faint
# 23      Not italic, not Fraktur
# 24      Underline: None    | not singly or doubly underlined
# 25      Blink: off
# 26      Reserved
# 27      Image: Positive
# 28      Reveal    | conceal off
# 29      Not crossed out
# 30-37   Set text color    | 30 + x, where x is from the color table below
# 38      Set xterm-256 text color    | next arguments are 5;x where x is color index (0..255)
# 39      Default text color    | implementation defined (according to standard)
# 40-47   Set background color    | 40 + x, where x is from the color table below
# 48      Set xterm-256 background color    | next arguments are 5;x where x is color index (0..255)
# 49      Default background color    | implementation defined (according to standard)
# 50      Reserved
# 51      Framed
# 52      Encircled
# 53      Overlined
# 54      Not framed or encircled
# 55      Not overlined
# 56-59   Reserved
# 60      ideogram underline or right side line    | hardly ever supported
# 61      ideogram double underline or double line on the right side    | hardly ever supported
# 62      ideogram overline or left side line    | hardly ever supported
# 63      ideogram double overline or double line on the left side    | hardly ever supported
# 64      ideogram stress marking    | hardly ever supported
# 90-99   Set foreground color, high intensity    | aixterm (not in standard)
# 100-109 Set background color, high intensity    | aixterm (not in standard)
#
#####################################################################################################

from enum import IntEnum, StrEnum

####################################################################################################

DEBUG_ANSI = False

####################################################################################################

class C0ControlCodes(StrEnum):
    # https://en.wikipedia.org/wiki/ASCII
    # first 32 characters of 128 ASCII 7-bit
    # NULL = 0
    BELL = '\a'   # 0x07
    BACKSPACE = '\b'   # 0x08
    TAB = '\t'   # 0x09
    LINEFEED = '\n'   # 0x0A
    FORMFEED = '\f'   # 0x0C
    CARRIAGE_RETURN = '\r'   # 0x0D
    ESCAPE = '\033'   # \e 0x1B
    # end of C0 block, then
    # SPACE = 0x20

class AnsiStyle(IntEnum):
    RESET = 0
    BRIGHT = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    # SLOW_BLINK = 5
    # RAPID_BLINK = 6
    INVERT = 7
    HIDE = 8
    STRIKE = 9
    # PRIMARY_FONT = 10
    # Alternative Font = 11 - 19
    # FRAKTUR = 20
    DOUBLY_UNDERLINED = 21
    NORMAL = 22
    # ...
    # 30–37 Set foreground color
    # 38    Set foreground color       Next arguments are 5;n or 2;r;g;b
    # 39    Default foreground color   Implementation defined (according to standard)
    # 40–47 Set background color
    # 48    Set background color       Next arguments are 5;n or 2;r;g;b
    # 49    Default background color   Implementation defined (according to standard)

class AnsiForeground(IntEnum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX = 90
    LIGHTRED_EX = 91
    LIGHTGREEN_EX = 92
    LIGHTYELLOW_EX = 93
    LIGHTBLUE_EX = 94
    LIGHTMAGENTA_EX = 95
    LIGHTCYAN_EX = 96
    LIGHTWHITE_EX = 97

class AnsiBackground(IntEnum):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    RESET = 49

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX = 100
    LIGHTRED_EX = 101
    LIGHTGREEN_EX = 102
    LIGHTYELLOW_EX = 103
    LIGHTBLUE_EX = 104
    LIGHTMAGENTA_EX = 105
    LIGHTCYAN_EX = 106
    LIGHTWHITE_EX = 107


# https://en.wikipedia.org/wiki/C0_and_C1_control_codes

# Control Sequence Introducer
CSI = C0ControlCodes.ESCAPE + '['   # C1 = 0x9B

# Operating System Command
OSC = C0ControlCodes.ESCAPE + ']'   # C1 = 0x9D

####################################################################################################

def escape_ansi(sequence: str) -> str:
    for a, b in (
        (C0ControlCodes.ESCAPE, '\\e'),
        (C0ControlCodes.BELL, '\\a'),
    ):
        sequence = sequence.replace(a, b)
    return sequence

def command(prefix: str, arg: str | int, code: str) -> str:
    if isinstance(arg, tuple):
        _ = ';'.join([str(_) for _ in arg])
    else:
        _ = str(arg)
    sequence = prefix + _ + str(code)
    if DEBUG_ANSI:
        print(escape_ansi(sequence))
    return sequence

def csi(*args) -> str:
    return command(CSI, *args)

def osc(*args) -> str:
    return command(OSC, *args)

# def csi(*args) -> str:
#     # arg: str | int, code: str
#     match len(args):
#         case 1:
#             return CSI + str(args[0])
#         case 2:
#             arg, code = args
#             if isinstance(arg, tuple):
#                 _ = ';'.join([str(_) for _ in arg])
#             else:
#                 _ = str(arg)
#             return CSI + _ + code
#     raise ValueError()


def cursor_up(n: int = 1) -> str:
    return csi(n, 'A')

def cursor_down(n: int = 1) -> str:
    return csi(n, 'B')

def cursor_forward(n: int = 1) -> str:
    return csi(n, 'C')

def cursor_backward(n: int = 1) -> str:
    return csi(n, 'D')

def cursor_next_line(n: int = 1) -> str:
    return csi(n, 'E')

def cursor_previous_line(n: int = 1) -> str:
    return csi(n, 'F')

def cursor_horizontal_absolute(n: int = 1) -> str:
    return csi(n, 'G')

def cursor_position(r: int = 1, c: int = 1) -> str:
    """Moves the cursor to row n, column m.

    The values are 1-based, and default to 1 (top left corner) if
    omitted. A sequence such as `CSI ;5H` is a synonym for `CSI 1;5H`
    as well as `CSI 17;H` is the same as `CSI 17H` and `CSI 17;1H`.

    """
    return csi((r, c), 'H')

def clear_screen(mode: int = 2) -> str:
    """Clears part of the screen.

    If n is 0 (or missing), clear from cursor to end of screen.
    If n is 1, clear from cursor to beginning of the screen.
    If n is 2, clear entire screen (and moves cursor to upper left on DOS ANSI.SYS).
    If n is 3, clear entire screen and delete all lines saved in the scrollback buffer
    (this feature was added for xterm and is supported by other terminal applications).
    """
    return csi(mode, 'J')

def clear_line(mode: int = 2) -> str:
    """Erases part of the line.

    If n is 0 (or missing), clear from cursor to the end of the line.
    If n is 1, clear from cursor to beginning of the line.
    If n is 2, clear entire line.
    Cursor position does not change.
    """
    return csi(mode, 'K')

def scroll_up(n: int = 1) -> str:
    return csi(n, 'S')

def scroll_down(n: int = 1) -> str:
    return csi(n, 'T')


def cursor_hv_position(n: int = 1, m: int = 1) -> str:
    """Same as `cursor_position`, but counts as a format effector function
    (like CR or LF) rather than an editor function (like `cursor_down` or `cursor_next_line`).
    This can lead to different handling in certain terminal modes.
    """
    return csi((n, m), 'f')


def sgr(*args) -> str:
    """Select Graphic Rendition"""
    return csi(args, 'm')


SGR_RESET = sgr(0)

# Reports the cursor position (CPR) by transmitting `ESC[n;mR`,
# where n is the row and m is the column.
REPORT_CURSOR_POSITION = csi(6, 'n')

REPORT_FOREGROUND_COLOR = osc((10, '?'), C0ControlCodes.BELL)   # '\033]10;?\007'
REPORT_BACKGROUND_COLOR = osc((11, '?'), C0ControlCodes.BELL)   # '\033]11;?\007'

def set_title(title: str) -> str:
    # Doesn't work with Konsole
    return osc((2, title), C0ControlCodes.BELL)
