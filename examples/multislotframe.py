import tkinter as tk
import tk_tools

root = tk.Tk()

msf = tk_tools.MultiSlotFrame(root)
msf.grid(row=0, column=0, sticky='news')

count = 0


def add_element():
    global count
    msf.add(count)
    count += 1


def show_elements():
    print(msf.get())


tk.Button(root, text='add element', command=add_element)\
    .grid(row=1, column=0, sticky='news')

tk.Button(root, text='retrieve elements', command=show_elements)\
    .grid(row=2, column=0, sticky='news')

root.mainloop()
