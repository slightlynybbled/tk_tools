import tkinter as tk
import tk_tools

import time

root = tk.Tk()

led = tk_tools.Led(root, size=50)
led.pack()

btn_red = tk.Button(root, text='red', command=led.to_red).pack(fill=tk.X)
btn_green = tk.Button(root, text='green', command=led.to_green).pack(fill=tk.X)
btn_grey = tk.Button(root, text='grey', command=led.to_grey).pack(fill=tk.X)

root.mainloop()
