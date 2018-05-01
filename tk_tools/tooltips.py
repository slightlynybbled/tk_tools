import tkinter as tk


class ToolTip(object):
    """
    Create a tooltip for a given widget
    """

    def __init__(self, widget, text='widget info'):
        self._widget = widget
        self._text = text
        self._widget.bind("<Enter>", self.enter)
        self._widget.bind("<Leave>", self.close)

        self._tw = None

    def enter(self, event=None):
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

    def close(self, event=None):
        if self._tw:
            self._tw.destroy()
