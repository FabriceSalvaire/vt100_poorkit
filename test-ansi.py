import sys

sdtout = sys.stdout

from vt100_toolkit.vt100 import *

for _ in range(100):
    print(_)

#! print(set_title('Title'))
print(clear_screen())
sdtout.write(cursor_position())
# print(clear_line(2))

print('Hello')

print(sgr(AnsiForeground.RED) + 'colour' + SGR_RESET)
print(sgr(AnsiBackground.RED) + 'colour' + SGR_RESET)
print(sgr(AnsiStyle.BRIGHT) + 'bright colour' + SGR_RESET)
print(sgr(AnsiStyle.FAINT) + 'faint colour' + SGR_RESET)
print(sgr(AnsiStyle.ITALIC) + 'colour' + SGR_RESET)
print(sgr(AnsiStyle.UNDERLINE) + 'colour' + SGR_RESET)
print(sgr(AnsiStyle.INVERT) + 'colour' + SGR_RESET)
print(sgr(AnsiStyle.HIDE) + 'colour' + SGR_RESET)
print(sgr(AnsiStyle.STRIKE) + 'colour' + SGR_RESET)
print(sgr(AnsiStyle.DOUBLY_UNDERLINED) + 'colour' + SGR_RESET)

sdtout.write('azerty')
sdtout.write(cursor_backward())
sdtout.write('1234')
sdtout.write(cursor_backward())
sdtout.write('5')
# sdtout.write(cursor_previous_line(5))
# sdtout.write('qsdf')
sdtout.write(cursor_position(10, 20))
sdtout.write('qsdf')

print()
