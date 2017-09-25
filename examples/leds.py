import tkinter as tk
import tk_tools

root = tk.Tk()

led = tk_tools.Led(root, size=50)
led.pack()

tk.Button(root, text='red', command=led.to_red).pack(fill=tk.X)
tk.Button(root, text='red on', command=lambda: led.to_red(True)).pack(fill=tk.X)
tk.Button(root, text='green', command=led.to_green).pack(fill=tk.X)
tk.Button(root, text='green on', command=lambda: led.to_green(True)).pack(fill=tk.X)
tk.Button(root, text='green', command=led.to_yellow).pack(fill=tk.X)
tk.Button(root, text='green on', command=lambda: led.to_yellow(True)).pack(fill=tk.X)
tk.Button(root, text='grey', command=led.to_grey).pack(fill=tk.X)

root.mainloop()
