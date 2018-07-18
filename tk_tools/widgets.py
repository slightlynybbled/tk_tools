import tkinter as tk
import tkinter.ttk as ttk
import logging

logger = logging.getLogger(__name__)


class SmartWidget(ttk.Frame):
    """
    Superclass which contains basic elements of the 'smart' widgets.
    """
    def __init__(self, parent):
        self._parent = parent
        super().__init__(self._parent)

        self._var = None

    def add_callback(self, callback: callable):
        """
        Add a callback on change

        :param callback: callable function
        :return: None
        """
        def internal_callback(*args):
            try:
                callback()
            except TypeError:
                callback(self.get())

        self._var.trace('w', internal_callback)

    def get(self):
        """
        Retrieve the value of the dropdown

        :return: the value of the current variable
        """
        return self._var.get()

    def set(self, value):
        """
        Set the value of the dropdown

        :param value: a string representing the
        :return: None
        """
        self._var.set(value)


class SmartOptionMenu(SmartWidget):
    """
    Classic drop down entry with built-in tracing variable.::

        # create the dropdown and grid
        som = SmartOptionMenu(root, ['one', 'two', 'three'])
        som.grid()

        # define a callback function that retrieves
        # the currently selected option
        def callback():
        print(som.get())

        # add the callback function to the dropdown
        som.add_callback(callback)

    :param data: the tk parent frame
    :param options: a list containing the drop down options
    :param initial_value: the initial value of the dropdown
    :param callback: a function
    """
    def __init__(self, parent, options: list, initial_value: str=None,
                 callback: callable=None):
        super().__init__(parent)

        self._var = tk.StringVar()
        self._var.set(initial_value if initial_value else options[0])

        self.option_menu = tk.OptionMenu(self, self._var,
                                         *options)
        self.option_menu.grid(row=0, column=0)

        if callback is not None:
            def internal_callback(*args):
                try:
                    callback()
                except TypeError:
                    callback(self.get())
            self._var.trace('w', internal_callback)


class SmartSpinBox(SmartWidget):
    """
    Easy-to-use spinbox.  Takes most options that work with a normal SpinBox.
    Attempts to call your callback function - if assigned - whenever there
    is a change to the spinbox.::

        # create a callback function
        def callback(value):
            print('the new value is: ', value)

        # create the smart spinbox and grid
        ssb = SmartSpinBox(root, from_=0, to=5, callback=callback)
        ssb.grid()

    :param parent: the tk parent frame
    :param entry_type: 'str', 'int', 'float'
    :param callback: python callable
    :param options: any options that are valid for tkinter.SpinBox
    """
    def __init__(self, parent, entry_type: str='float',
                 callback: callable=None, **options):
        """
        Constructor for SmartSpinBox
        """
        self._parent = parent
        super().__init__(self._parent)

        sb_options = options.copy()

        if entry_type == 'str':
            self._var = tk.StringVar()
        elif entry_type == 'int':
            self._var = tk.IntVar()
        elif entry_type == 'float':
            self._var = tk.DoubleVar()
        else:
            raise ValueError('Entry type must be "str", "int", or "float"')

        sb_options['textvariable'] = self._var
        self._spin_box = tk.Spinbox(self, **sb_options)
        self._spin_box.grid()

        if callback is not None:
            def internal_callback(*args):
                try:
                    callback()
                except TypeError:
                    callback(self.get())
            self._var.trace('w', internal_callback)


class SmartCheckbutton(SmartWidget):
    """
    Easy-to-use check button.  Takes most options that work with
    a normal CheckButton. Attempts to call your callback
    function - if assigned - whenever there is a change to
    the check button.::

        # create the smart spinbox and grid
        scb = SmartCheckbutton(root)
        scb.grid()

        # define a callback function that retrieves
        # the currently selected option
        def callback():
            print(scb.get())

        # add the callback function to the checkbutton
        scb.add_callback(callback)

    :param parent: the tk parent frame
    :param callback: python callable
    :param options: any options that are valid for tkinter.Checkbutton
    """
    def __init__(self, parent, callback: callable=None, **options):
        self._parent = parent
        super().__init__(self._parent)

        self._var = tk.BooleanVar()
        self._cb = tk.Checkbutton(self, variable=self._var, **options)
        self._cb.grid()

        if callback is not None:
            def internal_callback(*args):
                try:
                    callback()
                except TypeError:
                    callback(self.get())
            self._var.trace('w', internal_callback)


class BinaryLabel(ttk.Label):
    """
    Displays a value binary. Provides methods for
    easy manipulation of bit values.::

        # create the label and grid
        bl = BinaryLabel(root, 255)
        bl.grid()

        # toggle highest bit
        bl.toggle_msb()

    :param parent: the tk parent frame
    :param value: the initial value, default is 0
    :param options: prefix string for identifiers
    """
    def __init__(self, parent, value: int=0, prefix: str="", bit_width=8,
                 **options):
        self._parent = parent
        super().__init__(self._parent, **options)

        self._value = value
        self._prefix = prefix
        self._bit_width = bit_width
        self._text_update()

    def get(self):
        """
        Return the current value

        :return: the current integer value
        """
        return self._value

    def set(self, value: int):
        """
        Set the current value

        :param value:
        :return: None
        """
        max_value = int(''.join(['1' for _ in range(self._bit_width)]), 2)

        if value > max_value:
            raise ValueError('the value {} is larger than '
                             'the maximum value {}'.format(value, max_value))

        self._value = value
        self._text_update()

    def _text_update(self):
        self["text"] = \
            self._prefix +\
            str(bin(self._value))[2:].zfill(self._bit_width)[-self._bit_width:]

    def get_bit(self, position: int):
        """
        Returns the bit value at position

        :param position: integer between 0 and <width>, inclusive
        :return: the value at position as a integer
        """

        if position > (self._bit_width - 1):
            raise ValueError('position greater than the bit width')

        if self._value & (1 << position):
            return 1
        else:
            return 0

    def toggle_bit(self, position: int):
        """
        Toggles the value at position

        :param position: integer between 0 and 7, inclusive
        :return: None
        """
        if position > (self._bit_width - 1):
            raise ValueError('position greater than the bit width')

        self._value ^= (1 << position)
        self._text_update()

    def set_bit(self, position: int):
        """
        Sets the value at position

        :param position: integer between 0 and 7, inclusive
        :return: None
        """
        if position > (self._bit_width - 1):
            raise ValueError('position greater than the bit width')

        self._value |= (1 << position)
        self._text_update()

    def clear_bit(self, position: int):
        """
        Clears the value at position

        :param position: integer between 0 and 7, inclusive
        :return: None
        """
        if position > (self._bit_width - 1):
            raise ValueError('position greater than the bit width')

        self._value &= ~(1 << position)
        self._text_update()

    def get_msb(self):
        """
        Returns the most significant bit as an integer
        :return: the MSB
        """
        return self.get_bit(self._bit_width-1)

    def toggle_msb(self):
        """
        Changes the most significant bit
        :return: None
        """
        self.toggle_bit(self._bit_width-1)

    def get_lsb(self):
        """
        Returns the least significant bit as an integer
        :return: the LSB
        """
        return self.get_bit(0)

    def set_msb(self):
        """
        Sets the most significant bit
        :return: None
        """
        self.set_bit(self._bit_width-1)

    def clear_msb(self):
        """
        Clears the most significant bit
        :return: None
        """
        self.clear_bit(self._bit_width-1)

    def toggle_lsb(self):
        """
        Toggles the least significant bit
        :return:
        """
        self.toggle_bit(0)

    def set_lsb(self):
        """
        Sets the least significant bit
        :return: None
        """
        self.set_bit(0)

    def clear_lsb(self):
        """
        Clears the least significant bit
        :return: None
        """
        self.clear_bit(0)


class ByteLabel(BinaryLabel):
    """
    Has been replaced with more general BinaryLabel.
    Still here for backwards compatibility.
    """
    pass
