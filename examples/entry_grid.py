import tkinter as tk
import tk_tools

root = tk.Tk()

entry_grid = tk_tools.EntryGrid(root, 3, ['L0', 'L1', 'L2'])
entry_grid.grid(row=0, column=0)


def add_row():
    entry_grid.add_row()


def remove_row():
    entry_grid.remove_row(0)


def read():
    print(entry_grid.read(as_dicts=False))


add_row_btn = tk.Button(text='Add Row', command=add_row)
add_row_btn.grid(row=1, column=0, sticky='EW')

remove_row_btn = tk.Button(text='Remove Row', command=remove_row)
remove_row_btn.grid(row=2, column=0, sticky='EW')

read_btn = tk.Button(text='Read', command=read)
read_btn.grid(row=3, column=0, sticky='EW')

root.mainloop()
