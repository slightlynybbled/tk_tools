import tkinter as tk
import tk_tools

root = tk.Tk()

label_grid = tk_tools.LabelGrid(root, 3, ['Column0', 'Column1', 'Column2'])
label_grid.grid(row=0, column=0)


def add_row():
    row = [1, 2, 3]
    label_grid.add_row(row)


def remove_row():
    label_grid.remove_row(0)

add_row_btn = tk.Button(text='Add Row', command=add_row)
add_row_btn.grid(row=1, column=0, sticky='EW')

remove_row_btn = tk.Button(text='Remove Row', command=remove_row)
remove_row_btn.grid(row=2, column=0, sticky='EW')

root.mainloop()
