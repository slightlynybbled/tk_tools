import tkinter as tk


class ToolTip(object):
    """
    Add a tooltip to any widget.::

        entry = tk.Entry(root)
        entry.grid()

        # createst a tooltip
        tk_tools.ToolTip(entry, 'enter a value between 1 and 10')

    :param widget: the widget on which to hover
    :param text: the text to display
    :param time: the time to display the text, in milliseconds
    """

    def __init__(self, widget, text='widget info', time: int=4000):
        self._widget = widget
        self._text = text
        self._time = time

        self._widget.bind("<Enter>",
                          lambda _: self._widget.after(500, self._enter()))
        self._widget.bind("<Leave>", self._close)

        self._tw = None

    def _enter(self, event=None):
        x, y, cx, cy = self._widget.bbox("insert")
        x += self._widget.winfo_rootx() + 25
        y += self._widget.winfo_rooty() + 20

        # creates a toplevel window
        self._tw = tk.Toplevel(self._widget)

        # Leaves only the label and removes the app window
        self._tw.wm_overrideredirect(True)
        self._tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self._tw, text=self._text, justify='left',
                         background='#FFFFDD', relief='solid', borderwidth=1,
                         font=("times", "8", "normal"))

        label.pack(ipadx=1)

        if self._time:
            self._tw.after(self._time, self._tw.destroy)

    def _close(self, event=None):
        if self._tw:
            self._tw.destroy()
