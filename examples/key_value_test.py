import tkinter as tk
import tk_tools

root = tk.Tk()

kv = tk_tools.KeyValueEntry(root)
kv.pack()

kv.add(key='key0')
kv.add(key='key1')
kv.add(key='key2')

root.mainloop()
