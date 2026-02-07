from vt100_toolkit.terminal import Terminal
from vt100_toolkit.vt100 import sgr, SGR_RESET, AnsiStyle, AnsiForeground

terminal = Terminal(debug=True)
# terminal.clear()
# terminal.send(ansi.set_title('Title'))

terminal.print('message')
terminal.print(sgr(AnsiForeground.RED) + 'colour' + SGR_RESET)
terminal.print(sgr(AnsiStyle.BLINK) + 'text' + sgr(AnsiStyle.NOT_BLINK) + ' text' + SGR_RESET)
terminal.printc('<red>colour</>')
terminal.printc('<red>red</> <green>green</> <blue_light>blue</>')
terminal.print()
print('cursor', terminal.cursor_position)
print('size', terminal.size)
print('background', terminal.background_color)
print('foreground', terminal.foreground_color)
print('dark ?', terminal.is_dark_background)
# terminal.print()
