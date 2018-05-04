import tkinter as tk
import tk_tools


# this callback doesn't necessarily have to take the 'value', but it is considered good practice
def callback(value):
    print(value)


if __name__ == '__main__':

    root = tk.Tk()

    tk.Label(root, text="The variable value: ").grid(row=0, column=0)
    value_label = tk.Label(root, text="")
    value_label.grid(row=0, column=1)

    def callback(value):
        value_label.config(text=str(value))

    drop_down = tk_tools.SmartOptionMenu(root, ['one', 'two', 'three'], callback=callback)
    drop_down.grid()

    root.mainloop()
