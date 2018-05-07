import tkinter as tk
import tk_tools

from random import randint


def add_row():
    row = [randint(0, 10) for _ in range(3)]
    label_grid.add_row(row)


if __name__ == '__main__':

    root = tk.Tk()

    add_row_btn = tk.Button(text='Add Row', command=add_row)
    add_row_btn.grid(row=0, column=0, columnspan=2, sticky='ew')

    remove_row_btn = tk.Button(text='Remove Row')
    remove_row_btn.grid(row=1, column=0, sticky='ew')

    row_to_remove_entry = tk.Entry(root)
    row_to_remove_entry.grid(row=1, column=1, sticky='ew')
    row_to_remove_entry.insert(0, '0')

    remove_row_btn.config(command=lambda: label_grid.remove_row(int(row_to_remove_entry.get())))

    label_grid = tk_tools.LabelGrid(root, 3, ['Column0', 'Column1', 'Column2'])
    label_grid.grid(row=2, column=0, columnspan=2, sticky='ew')

    root.mainloop()
