import tkinter as tk
import tk_tools


# this callback doesn't necessarily have to take the 'value', but it is considered good practice
def callback(value):
    print(value)


if __name__ == '__main__':

    root = tk.Tk()

    drop_down = tk_tools.SmartOptionMenu(root, ['one', 'two', 'three'])
    drop_down.grid()

    drop_down.add_callback(callback)

    root.mainloop()
