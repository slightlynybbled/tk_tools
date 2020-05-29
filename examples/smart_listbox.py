import tkinter as tk
import tk_tools


if __name__ == '__main__':
    root = tk.Tk()

    tk.Label(root, text="The variable value: ").grid(row=0, column=0)
    value_label = tk.Label(root, text="")
    value_label.grid(row=0, column=1)

    def callback(values):
        string = ''.join(values)
        value_label.config(text=string)

    tk.Label(root, text='selectmode="browse"').grid(row=1, column=0)
    tk_tools.SmartListBox(root, on_select_callback=callback, selectmode='browse',
                          options=['1', '2', '3']).grid(row=2, column=0)

    tk.Label(root, text='selectmode="multiple"').grid(row=1, column=0)
    tk_tools.SmartListBox(root, on_select_callback=callback, selectmode='multiple',
                          options=['a', 'b', 'c']).grid(row=4, column=0)
    root.mainloop()
