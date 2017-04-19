import tkinter as tk


class DropDown(tk.OptionMenu):
    """
    Classic drop down entry
    
    Example use:
        # create the dropdown and grid
        dd = DropDown(root, ['one', 'two', 'three'])
        dd.grid()
    
        # define a callback function that retrieves the currently selected option
        def callback():
            print(dd.get())
            
        # add the callback function to the dropdown
        dd.add_callback(callback)
    """
    def __init__(self, parent, options: list):
        """
        Constructor for drop down entry
        
        :param parent: the tk parent frame
        :param options: a list containing the drop down options
        :param callback: a function to be executed when the dropdown changes
        """
        self.var = tk.StringVar(parent)
        self.var.set(options[0])

        self.option_menu = tk.OptionMenu.__init__(self, parent, self.var, *options)

        self.callback = None

    def add_callback(self, callback):
        def internal_callback(*args):
            callback()

        self.var.trace("w", internal_callback)

    def get(self):
        return self.var.get()

if __name__ == '__main__':
    root = tk.Tk()

    dd = DropDown(root, ['one', 'two', 'three'])
    dd.grid()

    def callback():
        print(dd.get())
    dd.add_callback(lambda: print(dd.get()))


    root.mainloop()
