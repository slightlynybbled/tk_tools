import tkinter as tk
import tk_tools
import random
import string


def random_letters():
    sal = string.ascii_letters
    return (random.choice(sal)
            + random.choice(sal)
            + random.choice(sal))


def add_row_random():
    r1 = random_letters()
    r2 = random_letters()
    r3 = random_letters()

    button_grid.add_row(
        [
            (r1, lambda: print(r1)),
            (r2, lambda: print(r2)),
            (r3, lambda: print(r3))
        ]
    )


def remove_row():
    button_grid.remove_row()


if __name__ == '__main__':

    root = tk.Tk()

    button_grid = tk_tools.ButtonGrid(root, 3, ['Column0', 'Column1', 'Column2'])
    button_grid.grid(row=0, column=0)

    add_row_btn2 = tk.Button(text='Add button row (random text)',
                             command=add_row_random)
    add_row_btn2.grid(row=1, column=0, sticky='EW')

    rm_row_btn = tk.Button(text='Remove button row', command=remove_row)
    rm_row_btn.grid(row=2, column=0, sticky='EW')

    root.mainloop()
