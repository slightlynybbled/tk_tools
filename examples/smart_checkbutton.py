import tkinter as tk
import tk_tools


# this callback doesn't necessarily have to take the 'value', but it is considered good practice
def callback(value):
    print(value)


if __name__ == '__main__':

    root = tk.Tk()

    scb = tk_tools.SmartCheckbutton(root)
    scb.grid()

    scb.add_callback(callback)

    root.mainloop()
