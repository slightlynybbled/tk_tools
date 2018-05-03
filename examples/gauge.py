import tkinter as tk
import tk_tools


root = tk.Tk()

max_speed = 20.0
speed_gauge = tk_tools.Gauge(root,
                             max_value=max_speed,
                             label='speed', unit='km/h')
speed_gauge.grid(row=0, column=0, sticky='news')


tach_gauge = tk_tools.Gauge(root,
                            max_value=8.0,
                            label='tach', unit='kRPM',
                            divisions=10)
tach_gauge.grid(row=1, column=0, sticky='news')

strange_gauge = tk_tools.Gauge(root,
                               max_value=30.0,
                               label='strange', unit='blah',
                               divisions=3)
strange_gauge.grid(row=2, column=0, sticky='news')

count = 0
up = True


def update_gauge():
    global count, up

    if up:
        count += 1.0
        if count > max_speed:
            up = False
    else:
        count -= 1.0

        if count <= 0.0:
            up = True

    speed_gauge.set_value(count)
    tach_gauge.set_value(count)
    strange_gauge.set_value(count)

    root.after(30, update_gauge)


root.after(100, update_gauge)

root.mainloop()
