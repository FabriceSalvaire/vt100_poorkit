This Python packages provides an API to support **VT100 Terminal**, aka UNIX terminal or console.

VT100 is a seventies computer standard for [terminal](https://en.wikipedia.org/wiki/VT100).  VT100
is a kind of prehistoric CSS.  It is still useful when you are too lazy to write a Qt QML or web
application, or you want to run your application in a SSH shell session.

I strongly recommend to look at the related packages (e.g. **prompt_toolkit**, **rich**) if you want
to build a sophisticated terminal user interface application.

In comparison to the related packages, this package implements new things or differently... Well it
is a bunch of opinionated codes to provide an alternative to opinionated codes...

There are also many ANSI Escape Sequence libraries like
[colorama](https://github.com/tartley/colorama) but they are usually limited to basic features.

For **Windows user**, as opposite to UNIX paradigm, Windows implemented a Win32 API to manage the
terminal. However, Windows 11 provides now the **Windows Terminal** which supports the VT100
protocol.  Thus, we can get rid of the VT100 / Win32 interface and only implements VT100.

It features:
- ANSI Escape Sequence
- True Colour RGB 8-bit
- terminal clear screen or line and cursor position
- **query terminal cursor position, size, foreground and background colour** (look at the code to see the UNIX TTY magic)

It don't features:
- old WIN32 API support
- old colour terminals
- mouse support (look related packages)

This code was (only) tested on Linux KDE **Konsole** terminal.

# Related packages

## Terminal UI Applications

[Python Prompt Toolkit](https://python-prompt-toolkit.readthedocs.io) (prompt_toolkit) is cool if
you want to implement a Command Line Interface (CLI) like IPyton, featuring completion.  However, it
is limited for rich text.

[Rich](https://rich.readthedocs.io/en/stable) is a kind of CSS engine for the terminal.  However, it
is a bit opinionated.  [Textual](https://textual.textualize.io) is written by the same developer.

**Currated Links:**
- [prompt-toolkit/python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)
  Library for building powerful interactive command line applications in Python

  [Terminal interface using prompt_toolkit? · Issue #8489 · ipython/ipython](https://github.com/ipython/ipython/issues/8489)
  [Related projects](https://python-prompt-toolkit.readthedocs.io/en/3.0.52/pages/related_projects.html)

- [Textualize/rich](https://github.com/Textualize/rich)

  Python library for writing rich text (with color and style) to the terminal, and for displaying
  advanced content such as tables, markdown, and syntax highlighted code.

- [Textual](https://textual.textualize.io)
  [Textualize/textual](https://github.com/Textualize/textual)
  
  The lean application framework for Python. Build sophisticated user interfaces with a simple
  Python API. Run your apps in the terminal and a web browser.

  Rapid Application Development framework for Python.
  Amazing examples !
  Based on **Rich**

- [Urwid](https://urwid.org)
  Console user interface library for Python
- [thomasballinger/curtsies](https://github.com/thomasballinger/curtsies)
  Curses-like terminal wrapper with a display based on compositing 2d arrays of text.
- [npyscreen](https://www.npcole.com/npyscreen)

**Followings are well-known UNIX Libraries:**
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
