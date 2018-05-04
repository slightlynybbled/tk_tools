import tkinter as tk
import tk_tools

from tk_tools.images import rotary_gauge_volt


def increment():
    global value
    value += increment_value

    p1.set_value(value)
    p2.set_value(value)


def decrement():
    global value
    value -= increment_value

    p1.set_value(value)
    p2.set_value(value)


if __name__ == '__main__':

    root = tk.Tk()

    p1 = tk_tools.RotaryScale(root, max_value=100.0, size=100, unit='km/h')
    p1.grid(row=0, column=0)

    p2 = tk_tools.RotaryScale(root,
                              max_value=100.0,
                              size=100,
                              needle_thickness=3,
                              needle_color='black',
                              img_data=rotary_gauge_volt)

    p2.grid(row=0, column=1)

    increment_value = 1.0
    value = 0.0

    inc_btn = tk.Button(root,
                        text='increment_value by {}'.format(increment_value),
                        command=increment)

    inc_btn.grid(row=1, column=0, columnspan=2, sticky='news')

    dec_btn = tk.Button(root,
                        text='decrement by {}'.format(increment_value),
                        command=decrement)

    dec_btn.grid(row=2, column=0, columnspan=2, sticky='news')

    root.mainloop()
