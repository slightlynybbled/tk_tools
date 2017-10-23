import tkinter as tk
import tk_tools

root = tk.Tk()

button_grid = tk_tools.ButtonGrid(root, 3, ['Column0', 'Column1', 'Column2'])
button_grid.grid(row=0, column=0)


def add_row():
    button_grid.add_row()


add_row_btn = tk.Button(text='Add button row', command=add_row)
add_row_btn.grid(row=1, column=0, sticky='EW')

root.mainloop()
