import tkinter as tk
import tk_tools
from decimal import Decimal


root = tk.Tk()

max_speed = 20.0

ss_float = tk_tools.SevenSegmentDigits(root, digits=5)
ss_float.grid(row=0, column=1, sticky='news')

ss_int = tk_tools.SevenSegmentDigits(root, digits=3, background='black', digit_color='red')
ss_int.grid(row=1, column=1, sticky='news')

count = 0
up = True


def update_gauge():
    global count, up

    if up:
        count += 0.1
        if count > max_speed:
            up = False
    else:
        count -= 0.1

        if count < -1.0:
            up = True

    decimal_count_float = str(Decimal(count).quantize(Decimal('0.10')))
    decimal_count_int = str(Decimal(count).quantize(Decimal('1')))

    ss_float.set_value(decimal_count_float)
    ss_int.set_value(decimal_count_int)

    root.after(100, update_gauge)


root.after(100, update_gauge)

root.mainloop()
