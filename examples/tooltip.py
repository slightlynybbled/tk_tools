import tkinter as tk
import tk_tools

root = tk.Tk()

tk.Label(root, text='Hover over the labels and controls in order to raise a tool tip').grid(row=0, column=0)

entry = tk.Entry(root)
entry.grid(row=1, column=0, sticky='news')
tk_tools.ToolTip(entry, 'enter some data here')


def btn_press():
    print(entry.get())
    entry.delete(0, 'end')


button = tk.Button(root, text='the button', command=btn_press)
button.grid(row=2, column=0, sticky='news')
tk_tools.ToolTip(button, 'press the button!')

root.mainloop()
