import tkinter as tk
import tk_tools
import random
import string

root = tk.Tk()

button_grid = tk_tools.ButtonGrid(root, 3, ['Column0', 'Column1', 'Column2'])
button_grid.grid(row=0, column=0)

row = 1

def random_letters():
	sal = string.ascii_letters
	return random.choice(sal) + random.choice(sal) + random.choice(sal)

def add_row():
	global row
	button_grid.add_row([(0, 'A'+str(row), None), (1, 'B'+str(row), None), (2, 'C'+str(row), None)])
	row += 1

def add_row_random():
	r1 = random_letters()
	r2 = random_letters()
	r3 = random_letters()
	f1 = lambda: print(r1)
	f2 = lambda: print(r2)
	f3 = lambda: print(r3)
	button_grid.add_row([(0, r1, f1), (1, r2, f2), (2, r3, f3)])

add_row_btn1 = tk.Button(text='Add button row (cell text)', command=add_row)
add_row_btn1.grid(row=1, column=0, sticky='EW')

add_row_btn2 = tk.Button(text='Add button row (random text)', command=add_row_random)
add_row_btn2.grid(row=2, column=0, sticky='EW')

root.mainloop()
