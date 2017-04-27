import tkinter as tk
import tk_tools

root = tk.Tk()

btn_img = tk.PhotoImage(file='./img/rotary-scale.png')
btn = tk.Button(root, image=btn_img)
btn.grid()

root.mainloop()
