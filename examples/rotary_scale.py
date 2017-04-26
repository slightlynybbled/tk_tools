import tkinter as tk
import tk_tools

root = tk.Tk()

p = tk_tools.RotaryScale(root, range=20.0)
p.grid(row=0, column=0)

increment = 1.0
value = 0.0


def inc():
    global value
    value += increment
    p.arrow(value)
    print(value)


def dec():
    global value
    value -= increment
    p.arrow(value)
    print(value)


inc_btn = tk.Button(root, text='increment by {}'.format(increment), command=inc)
inc_btn.grid(row=1, column=0)
dec_btn = tk.Button(root, text='decrement by {}'.format(increment), command=dec)
dec_btn.grid(row=2, column=0)

root.mainloop()