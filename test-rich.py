####################################################################################################

import time

from rich.console import Console, OverflowMethod
from rich.json import JSON
from rich.__main__ import make_test_card

# Console API

console = Console()
print(console.size)
print(console.encoding)
print(console.is_terminal)
print(console.color_system)

# Printing

print()
console.print([1, 2, 3])
console.print("[blue underline]Looks like a link")
console.print(locals())
console.print("FOO", style="white on blue")

# Logging

print()
console.log("Hello, World!")

# Printing JSON

print()
console.print_json('[false, true, null, "foo"]')
console.log(JSON('["foo", "bar"]'))

# Low level output

print()
console.out("Locals", locals())

# Rules

print()
console.rule("[bold red]Chapter 2")

# Status

print()
i = 0
with console.status("Working..."):   # , spinner=''
    while i < 10:
        time.sleep(.1)
        i += 1

# Justify / Alignment

print()
style = "bold white on blue"
console.print("Rich", style=style)
console.print("Rich", style=style, justify="left")
console.print("Rich", style=style, justify="center")
console.print("Rich", style=style, justify="right")

# Overflow

print()
console = Console(width=14)
supercali = "supercalifragilisticexpialidocious"
overflow_methods: list[OverflowMethod] = ["fold", "crop", "ellipsis"]
for overflow in overflow_methods:
    console.rule(overflow)
    console.print(supercali, overflow=overflow, style="bold blue")
    console.print()

console = Console()

# Console style

print()
blue_console = Console(style="white on blue")
blue_console.print("I'm blue. Da ba dee da ba di.")

# Soft Wrapping
# Cropping

# Input

## console = Console()
## console.input("What is [i]your[/i] [bold red]name[/]? :smiley: ")

# Exporting

## console = Console(record=True)

# Error console

## error_console = Console(stderr=True)

# File output

## with open('report.txt', 'wt') as report_file:
##     console = Console(file=report_file)
##     console.rule(f"Report Generated {datetime.now().ctime()}")

# Capturing output

with console.capture() as capture:
    console.print("[bold red]Hello[/] World")
str_output = capture.get()

## from io import StringIO
## console = Console(file=StringIO())
## console.print("[bold red]Hello[/] World")
## str_output = console.file.getvalue()

# Paging

with console.pager(styles=True):
    console.print(make_test_card())

# Alternate screen

## with console.screen():
##     console.print(locals())
##     time.sleep(5)
