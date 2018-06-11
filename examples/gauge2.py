import tkinter as tk
import tk_tools


root = tk.Tk()

max_speed = 20000

speed_gauge = tk_tools.Gauge2(root,
                             max_value=max_speed,
                             label='speed', unit=' m/h',bg='grey')
speed_gauge.grid(row=0, column=0, sticky='news')


tach_gauge = tk_tools.Gauge2(root,
                            max_value=8000,
                            label='tach', unit=' RPM',
                            divisions=10)
tach_gauge.grid(row=1, column=0, sticky='news')

strange_gauge = tk_tools.Gauge2(root,
                               max_value=30000,
                               label='strange', unit=' blah',
                               divisions=10, red=90, yellow=60)
strange_gauge.grid(row=2, column=0, sticky='news')

batV_gauge = tk_tools.Gauge2(root,       height=120, width=250,
                                max_value=16, min_value=8,
                                label='Bat voltage', unit='V',
                                divisions=8, yellow=60, red=75,
                                red_low=30, yellow_low=40)
batV_gauge.grid(row=0, column=1, sticky='news')

batI_gauge = tk_tools.Gauge2(root,       height=120, width=250,
                                max_value=6, min_value=-8,
                                label='Bat current', unit='A',
                                divisions=14, yellow=80, red=90,
                                red_low=20, yellow_low=30,bg='lavender')
batI_gauge.grid(row=1, column=1, sticky='news')

count = 0
up = True


def update_gauge():
    global count, up

    increment = 30

    if up:
        count += increment
        if count > max_speed:
            up = False
    else:
        count -= increment

        if count <= 0.0:
            up = True

    speed_gauge.set_value(count)
    tach_gauge.set_value(count)
    strange_gauge.set_value(count)
    batV_gauge.set_value(count/1000)
    batI_gauge.set_value((count-10000)/1000)

    root.after(50, update_gauge)


root.after(100, update_gauge)

root.mainloop()
