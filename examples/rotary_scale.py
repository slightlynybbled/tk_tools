import tkinter as tk
import tk_tools

from tk_tools.images import rotary_gauge_volt

root = tk.Tk()

p1 = tk_tools.RotaryScale(root, max_value=100.0, size=100, unit='km/h')
p1.grid(row=0, column=0)

p2 = tk_tools.RotaryScale(root, max_value=100.0, size=100, img_data=rotary_gauge_volt)
p2.grid(row=0, column=1)

increment = 1.0
value = 0.0


def inc():
    global value
    value += increment

    p1.set_value(value)
    p2.set_value(value)


def dec():
    global value
    value -= increment

    p1.set_value(value)
    p2.set_value(value)


inc_btn = tk.Button(root, text='increment by {}'.format(increment), command=inc)
inc_btn.grid(row=1, column=0, columnspan=2, sticky='news')

dec_btn = tk.Button(root, text='decrement by {}'.format(increment), command=dec)
dec_btn.grid(row=2, column=0, columnspan=2, sticky='news')

root.mainloop()
