import tkinter as tk


class SmartWidget:
    def __init__(self):
        self.var = None

    def add_callback(self, callback: callable):
        """
        Add a callback on change

        :param callback: callable function
        :return:
        """
        def internal_callback(*args):
            callback()

        self.var.trace('w', internal_callback)

    def get(self):
        """
        Retrieve the value of the dropdown

        :return:
        """
        return self.var.get()

    def set(self, value):
        """
        Set the value of the dropdown

        :param value: a string representing the
        :return:
        """
        self.var.set(value)


class SmartOptionMenu(tk.OptionMenu, SmartWidget):
    """
    Classic drop down entry

    Example use:
        # create the dropdown and grid
        som = SmartOptionMenu(root, ['one', 'two', 'three'])
        som.grid()

        # define a callback function that retrieves
        # the currently selected option
        def callback():
            print(som.get())

        # add the callback function to the dropdown
        som.add_callback(callback)
    """
    def __init__(self, parent, options: list, initial_value: str=None,
                 callback: callable=None):
        """
        Constructor for SmartOptionMenu entry

        :param parent: the tk parent frame
        :param options: a list containing the drop down options
        :param initial_value: the initial value of the dropdown
        :param callback: a function
        """
        self.var = tk.StringVar(parent)
        self.var.set(initial_value if initial_value else options[0])

        self.option_menu = tk.OptionMenu.__init__(self, parent, self.var,
                                                  *options)

        if callback is not None:
            def internal_callback(*args):
                callback()
            self.var.trace('w', internal_callback)


class SmartSpinBox(tk.Spinbox, SmartWidget):
    """
    Easy-to-use spinbox.  Takes most options that work with a normal SpinBox.
    Attempts to call your callback function - if assigned - whenever there
    is a change to the spinbox.

    Example use:
        # create the smart spinbox and grid
        ssb = SmartSpinBox(root)
        ssb.grid()

        # define a callback function that retrieves
        # the currently selected option
        def callback():
            print(ssb.get())

        # add the callback function to the spinbox
        ssb.add_callback(callback)
    """
    def __init__(self, parent, entry_type: str='float',
                 callback: callable=None, **options):
        """
        Constructor for SmartSpinBox

        :param parent: the tk parent frame
        :param entry_type: 'str', 'int', 'float'
        :param callback: python callable
        :param options: any options that are valid for tkinter.SpinBox
        """
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
    """
    Easy-to-use spinbox.  Takes most options that work with a normal SpinBox.
    Attempts to call your callback function - if assigned - whenever there
    is a change to the spinbox.

    Example use:
        # create the smart spinbox and grid
        scb = SmartCheckbutton(root)
        scb.grid()

        # define a callback function that retrieves
        # the currently selected option
        def callback():
            print(scb.get())

        # add the callback function to the checkbutton
        scb.add_callback(callback)
    """
    def __init__(self, parent, callback: callable=None, **options):
        """
        Constructor for SmartCheckbutton

        :param parent: the tk parent frame
        :param callback: python callable
        :param options: any options that are valid for tkinter.Checkbutton
        """
        self.var = tk.BooleanVar()
        super().__init__(parent, variable=self.var, **options)

        if callback is not None:
            def internal_callback(*args):
                callback()
            self.var.trace('w', internal_callback)
