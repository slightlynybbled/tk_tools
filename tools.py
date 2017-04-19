import tkinter as tk


class DropDown(tk.OptionMenu):
    def __init__(self, parent, options):
        self.var = tk.StringVar(parent)
        self.var.set(options[0])

        self.option_menu = tk.OptionMenu.__init__(self, parent, self.var, *options)

    def get(self):
        return self.var.get()

if __name__ == '__main__':
    root = tk.Tk()

    dd = DropDown(root, ['one', 'two', 'three'])
    dd.grid()

    root.mainloop()
