from vt100_toolkit.terminal import *
from vt100_toolkit.vt100 import *

terminal = Terminal(debug=True)
# terminal.clear()
# terminal.send(ansi.set_title('Title'))

terminal.print('message')
terminal.print(sgr(AnsiForeground.RED) + 'colour' + SGR_RESET)
terminal.printc('<red>colour</>')
terminal.printc('<red>colour</> <green>blue</>')
terminal.print()
print('cursor', terminal.cursor_position)
print('size', terminal.size)
print('background', terminal.background_color)
print('foreground', terminal.foreground_color)
print('dark ?', terminal.is_dark_background)
# terminal.print()
