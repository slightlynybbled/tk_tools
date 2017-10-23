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


class ByteLabel(tk.Label):
    """
    Displays a byte value binary. Provides methods for
    easy manipulation of bit values.

       Example use:
           # create the label and grid
           bl = ByteLabel(root, 255)
           bl.grid()

           # toggle highest bit
           bl.toggle_msb()
    """
    def __init__(self, parent, value=0, prefix="", **options):
        """
        Constructor for ByteLabel

        :param parent: the tk parent frame
        :param value: the initial value, default is 0
        :param options: prefix string for identifiers
        """
        super().__init__(parent, **options)
        assert -1 < value < 256
        self._value = value
        self._prefix = prefix
        self.text_update()

    def get(self):
        return self._value

    def set(self, value):
        assert -1 < value < 256
        self._value = value
        self.text_update()

    def text_update(self):
        self["text"] = self._prefix + str(bin(self._value))[2:].zfill(8)

    def get_bit(self, position):
        assert -1 < position < 8
        return self._value & (1 << position)

    def toggle_bit(self, position):
        assert -1 < position < 8
        self._value ^= (1 << position)
        self.text_update()

    def set_bit(self, position):
        assert -1 < position < 8
        self._value |= (1 << position)
        self.text_update()

    def clear_bit(self, position):
        assert -1 < position < 8
        self._value &= ~(1 << position)
        self.text_update()

    def get_msb(self):
        self.get_bit(7)

    def toggle_msb(self):
        self.toggle_bit(7)

    def get_lsb(self):
        self.get_bit(0)

    def set_msb(self):
        self.set_bit(7)

    def clear_msb(self):
        self.clear_bit(7)

    def toggle_lsb(self):
        self.toggle_bit(0)

    def set_lsb(self):
        self.set_bit(0)

    def clear_lsb(self):
        self.clear_bit(0)


if __name__ == '__main__':
    root = tk.Tk()
    '''
    ssb = SmartSpinBox(root, 'float', from_=0, to=5,
                       increment=0.1, callback=lambda: print('it works'))
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
