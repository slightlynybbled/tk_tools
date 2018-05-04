import tkinter as tk
import tk_tools
import random


def add_row():
    entry_grid.add_row()


def add_with_data():
    data = [random.randint(0, 10) for _ in range(3)]
    entry_grid.add_row(data=data)


def read():
    print(entry_grid.read(as_dicts=False))


if __name__ == '__main__':

    root = tk.Tk()

    add_row_btn = tk.Button(root, text='Add Row', command=add_row)
    add_row_btn.grid(row=0, column=0, columnspan=2, sticky='ew')

    add_row_data_btn = tk.Button(root, text='Add Row (with data)', command=add_with_data)
    add_row_data_btn.grid(row=1, column=0, columnspan=2, sticky='ew')

    remove_row_btn = tk.Button(root, text='Remove Row')
    remove_row_btn.grid(row=2, column=0, sticky='ew')

    row_to_remove_entry = tk.Entry(root)
    row_to_remove_entry.grid(row=2, column=1, sticky='ew')
    row_to_remove_entry.insert(0, '0')

    remove_row_btn.config(command=lambda: entry_grid.remove_row(int(row_to_remove_entry.get())))

    read_btn = tk.Button(root, text='Read', command=read)
    read_btn.grid(row=3, column=0, columnspan=2, sticky='ew')

    entry_grid = tk_tools.EntryGrid(root, 3, ['L0', 'L1', 'L2'])
    entry_grid.grid(row=4, column=0, columnspan=2, sticky='ew')

    root.mainloop()
