import tkinter as tk
import tk_tools


if __name__ == '__main__':
    root = tk.Tk()

    tk.Label(root, text="The variable value: ").grid(row=0, column=0)
    value_label = tk.Label(root, text="")
    value_label.grid(row=0, column=1)

    def callback(value):
        value_label.config(text=str(value))

    scb = tk_tools.SmartCheckbutton(root, callback=callback)
    scb.grid()

    root.mainloop()
