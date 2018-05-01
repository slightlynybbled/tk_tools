import tkinter as tk
import tkinter.ttk as ttk


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
        self.tw = tk.Toplevel(self._widget)

        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self._text, justify='left',
                         background='#FFFFDD', relief='solid', borderwidth=1,
                         font=("times", "8", "normal"))

        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()
