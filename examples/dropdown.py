import tkinter as tk
import tk_tools


def callback():
    print(drop_down.get())


if __name__ == '__main__':

    root = tk.Tk()

    drop_down = tk_tools.SmartOptionMenu(root, ['one', 'two', 'three'])
    drop_down.grid()

    drop_down.add_callback(callback)

    root.mainloop()
