import tkinter as tk
import tk_tools


def add_series():
    line_1 = [(x/5 - 1.0, x/10.0) for x in range(10)]
    graph.plot_line(line_1, point_visibility=True, color='blue')


def add_point():
    point = (0.5, 0.75)
    graph.plot_point(*point, color='red')


def clear():
    graph.draw_axes()


if __name__ == '__main__':

    root = tk.Tk()

    # create the graph
    graph = tk_tools.Graph(
        parent=root,
        x_min=-1.0,
        x_max=1.0,
        y_min=0.0,
        y_max=2.0,
        x_tick=0.2,
        y_tick=0.2,
        width=500,
        height=400
    )

    graph.grid(row=0, column=0)

    # create an initial line
    line_0 = [(x / 10, x / 10) for x in range(10)]
    graph.plot_line(line_0)

    add_series_btn = tk.Button(root, text='add series', command=add_series)
    add_series_btn.grid(row=1, column=0, sticky='EW')

    add_point_btn = tk.Button(root, text='add point', command=add_point)
    add_point_btn.grid(row=2, column=0, sticky='EW')

    clear_btn = tk.Button(root, text='clear', command=clear)
    clear_btn.grid(row=3, column=0, sticky='EW')

    root.mainloop()
