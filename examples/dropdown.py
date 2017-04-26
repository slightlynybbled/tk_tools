import tkinter as tk
import tk_tools

root = tk.Tk()

dd = tk_tools.DropDown(root, ['one', 'two', 'three'])
dd.grid()


def callback():
    print(dd.get())

dd.add_callback(lambda: print(dd.get()))

root.mainloop()
