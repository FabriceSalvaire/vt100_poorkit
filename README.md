This — experimental — Python packages provides an API to support **VT100 Terminal**, aka UNIX terminal or console.

I strongly recommend to look at
**[prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)** (or alternatives) to
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

# Relates packages

## Terminal UI Applications

- [prompt-toolkit/python-prompt-toolkit: Library for building powerful interactive command line applications in Python](https://github.com/prompt-toolkit/python-prompt-toolkit)
  [Terminal interface using prompt_toolkit? · Issue #8489 · ipython/ipython](https://github.com/ipython/ipython/issues/8489)
  [Related projects](https://python-prompt-toolkit.readthedocs.io/en/3.0.52/pages/related_projects.html)

- [Rich](https://rich.readthedocs.io/en/stable)
  Python library for writing rich text (with color and style) to the terminal, and for displaying
  advanced content such as tables, markdown, and syntax highlighted code.
  [Textualize/rich: Rich is a Python library for rich text and beautiful formatting in the terminal.](https://github.com/Textualize/rich)
- [Textual](https://textual.textualize.io)
  [Textualize/textual: The lean application framework for Python. Build sophisticated user interfaces with a simple Python API. Run your apps in the terminal and a web browser.](https://github.com/Textualize/textual)
  Rapid Application Development framework for Python.
  Amazing examples !
  Based on **Rich**

- [Urwid](https://urwid.org)
  Console user interface library for Python
- [thomasballinger/curtsies: Curses-like terminal wrapper with a display based on compositing 2d arrays of text.](https://github.com/thomasballinger/curtsies)
- [npyscreen](https://www.npcole.com/npyscreen)

- [Curses Programming with Python — Python 3 documentation](https://docs.python.org/3/howto/curses.html)
  [curses — Terminal handling for character-cell displays — Python 3 documentation](https://docs.python.org/3/library/curses.html#module-curses)
- [The GNU Readline Library](https://tiswww.case.edu/php/chet/readline/rltop.html)

## ANSI Escape Sequences

- [tartley/colorama: Simple cross-platform colored terminal text in Python](https://github.com/tartley/colorama)
  implements VT100 and Win32
- PyPI has a zillion of similar toy packages, it looks like a student hobby...

## ...

And found on PyPI, see `found-on-pypi.md`

# References

- [ECMA-48](https://ecma-international.org/publications-and-standards/standards/ecma-48)
- ISO/IEC 6429 Information technology — Control functions for coded character sets
