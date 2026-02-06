This — experimental — Python packages provides an API to support **VT100 Terminal**, aka UNIX terminal or console.

I strongly recommend to look at **[prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)** to
build sophisticated console user interface application.

In comparison to prompt-toolkit, this package implements new things or differently...

There are also many ANSI Escape Sequence libraries like
[colorama](https://github.com/tartley/colorama) but they are usually limited to basic things.

It features:
- ANSI Escape Sequence
- True Color printing
- terminal clear screen or line and cursor position
- **query terminal cursor position, size, foreground and background colour** (look at the code to see the UNIX TTY magic)

This code was tested on Linux KDE **Konsole** terminal.

For **Windows user**, as opposite to UNIX paradigm, Windows implements a Win32 API to manage the
terminal. However, Windows 11 provides now the **Windows Terminal** which supports the VT100
protocol.

# Notes on prompt-toolkit

Look at these files:
- `tools/debug_vt100_input.py`
- `src/prompt_toolkit/output/vt100.py`
- `src/prompt_toolkit/input/vt100.py`
- `src/prompt_toolkit/input/vt100_parser.py`

# Relates packages

## Terminal UI Applications

- [prompt-toolkit/python-prompt-toolkit: Library for building powerful interactive command line applications in Python](https://github.com/prompt-toolkit/python-prompt-toolkit)
  [Terminal interface using prompt_toolkit? · Issue #8489 · ipython/ipython](https://github.com/ipython/ipython/issues/8489)

- [Curses Programming with Python — Python 3 documentation](https://docs.python.org/3/howto/curses.html)
  [curses — Terminal handling for character-cell displays — Python 3 documentation](https://docs.python.org/3/library/curses.html#module-curses)
- [The GNU Readline Library](https://tiswww.case.edu/php/chet/readline/rltop.html)

## ANSI Escape Sequences

- [tartley/colorama: Simple cross-platform colored terminal text in Python](https://github.com/tartley/colorama)
  implements VT100 and Win32

## ...

And found on PyPI, see `found-on-pypi.md`, it looks like a student hobby ...

# References

- [ECMA-48 - Ecma International](https://ecma-international.org/publications-and-standards/standards/ecma-48)
- ISO/IEC 6429 Information technology — Control functions for coded character sets
