import tkinter as tk
import tk_tools

root = tk.Tk()

blabel1 = tk_tools.widgets.ByteLabel(root, 153, "d1:")
blabel1.grid(row=0, column=0)

e = tk.Entry(root, width=10)
e.grid(row=1, column=0)

btn_set = tk.Button(root, text="Set", command=lambda: blabel1.set_value(int(e.get())))
btn_set.grid(row=1, column=1)

btn_set = tk.Button(root, text="Toggle MSB", command=blabel1.toggle_msb)
btn_set.grid(row=1, column=2)

btn_set = tk.Button(root, text="Toggle LSB", command=blabel1.toggle_lsb)
btn_set.grid(row=1, column=3)

root.mainloop()
