import tkinter as tk


class SmartOptionMenu(tk.OptionMenu):
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
    def __init__(self, parent, options: list, initial_value: str=None, callback: callable=None):
        """
        Constructor for drop down entry
        
        :param parent: the tk parent frame
        :param options: a list containing the drop down options
        :param initial_value: the initial value of the dropdown
        :param callback: a function
        """
        self.var = tk.StringVar(parent)
        self.var.set(initial_value if initial_value else options[0])

        self.option_menu = tk.OptionMenu.__init__(self, parent, self.var, *options)

        def internal_callback(*args):
            callback()
        self.var.trace('w', internal_callback)

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


class SmartWidget:
    def __init__(self):
        self.var = None

    def add_callback(self, callback: callable):
        def internal_callback(*args):
            callback()

        self.var.trace('w', internal_callback)

    def get(self):
        return self.var.get()

    def set(self, value):
        self.var.set(value)


class SmartSpinBox(tk.Spinbox, SmartWidget):
    """
    Easy-to-use spinbox.  Takes most options that work with a normal SpinBox.
    Attempts to call your callback function - if assigned - whenever there
    is a change to the spinbox.

    Example use:
        # create the smart spinbox and grid
        ssb = SmartSpinBox(root, )
        ssb.grid()

        # define a callback function that retrieves the currently selected option
        def callback():
            print(ssb.get())

        # add the callback function to the dropdown
        ssb.add_callback(callback)
    """
    def __init__(self, parent, entry_type: str='float', callback: callable=None, **options):

        sb_options = options.copy()

        print('sb_options: ', sb_options)

        if entry_type == 'str':
            self.var = tk.StringVar()
        elif entry_type == 'int':
            self.var = tk.IntVar()

        elif entry_type == 'float':
            self.var = tk.DoubleVar()
        else:
            raise ValueError('Entry type must be "str", "int", or "float"')

        sb_options['textvariable'] = self.var
        super().__init__(parent, **sb_options)

        if callback is not None:
            def internal_callback(*args):
                callback()
            self.var.trace('w', internal_callback)


class SmartCheckbutton(tk.Checkbutton, SmartWidget):
    def __init__(self, parent, callback: callable=None, **options):

        self.var = tk.BooleanVar()
        super().__init__(parent, variable=self.var, **options)

        if callback is not None:
            def internal_callback(*args):
                callback()
            self.var.trace('w', internal_callback)


if __name__ == '__main__':
    root = tk.Tk()
    '''
    ssb = SmartSpinBox(root, 'float', from_=0, to=5, increment=0.1, callback=lambda: print('it works'))
    ssb.grid()

    print(ssb)

    def callback():
        print(ssb.get())

    ssb.add_callback(callback)
    '''
    scb = SmartCheckbutton(root, text='Enable')
    scb.grid()

    def callback():
        print(scb.get())

    scb.add_callback(callback)

    root.mainloop()
