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
    def __init__(self, parent, options: list, initial_value: str=None):
        """
        Constructor for drop down entry
        
        :param parent: the tk parent frame
        :param options: a list containing the drop down options
        :param initial_value: the initial value of the dropdown
        """
        self.var = tk.StringVar(parent)
        self.var.set(initial_value if initial_value else options[0])

        self.option_menu = tk.OptionMenu.__init__(self, parent, self.var, *options)

        self.callback = None

    def add_callback(self, callback: callable):
        """
        Add a callback on change
        
        :param callback: callable function
        :return: 
        """
        def internal_callback(*args):
            callback()

        self.var.trace("w", internal_callback)

    def get(self):
        """
        Retrieve the value of the dropdown
        
        :return: 
        """
        return self.var.get()

    def set(self, value: str):
        """
        Set the value of the dropdown
        
        :param value: a string representing the
        :return: 
        """
        self.var.set(value)

if __name__ == '__main__':
    root = tk.Tk()

    dd = DropDown(root, ['', 'one', 'two', 'three'])
    dd.grid()

    print(dd)

    def callback():
        print(dd.get())
    dd.add_callback(lambda: print(dd.get()))

    root.mainloop()
