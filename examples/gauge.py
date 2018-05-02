import tkinter as tk
import tk_tools


root = tk.Tk()

speed_gauge = tk_tools.Gauge(root,
                             max_value = 160.0,
                             label='speed', unit='km/h')
speed_gauge.grid(row=0, column=0, sticky='news')


tach_gauge = tk_tools.Gauge(root,
                            max_value = 8.0,
                            label='tach', unit='kRPM')
tach_gauge.grid(row=1, column=0, sticky='news')

speed_gauge.set_value(132.1)
tach_gauge.set_value(4.6)

root.mainloop()
