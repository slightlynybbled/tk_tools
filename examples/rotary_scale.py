import tkinter as tk
import tk_tools

root = tk.Tk()

p = tk_tools.RotaryScale(root, max_value=20.0, size=200)
p.grid(row=0, column=0)

increment = 1.0
value = 0.0


def inc():
    global value
    value += increment
    p.set_value(value)
    print(value)


def dec():
    global value
    value -= increment
    p.set_value(value)
    print(value)


inc_btn = tk.Button(root, text='increment by {}'.format(increment), command=inc)
inc_btn.grid(row=1, column=0)
dec_btn = tk.Button(root, text='decrement by {}'.format(increment), command=dec)
dec_btn.grid(row=2, column=0)

root.mainloop()
