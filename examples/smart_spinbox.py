import tkinter as tk
import tk_tools


if __name__ == '__main__':
    root = tk.Tk()

    tk.Label(root, text="The variable value: ").grid(row=0, column=0)
    value_label = tk.Label(root, text="")
    value_label.grid(row=0, column=1)

    def callback(value):
        value_label.config(text=str(value))

    # specify a callback, then specify the normal spinbox options (such as "from_", "to", and "increment"
    tk_tools.SmartSpinBox(root, callback=callback, entry_type='int',
                          from_=0, to=3).grid(row=1, column=0)
    tk_tools.SmartSpinBox(root, callback=callback, entry_type='float',
                          from_=-2.5, to=3.0, increment=0.1).grid(row=2, column=0)
    tk_tools.SmartSpinBox(root, callback=callback, entry_type='str',
                          values=('a', 'b', 'c')).grid(row=3, column=0)
    root.mainloop()
