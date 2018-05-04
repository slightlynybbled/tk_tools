import tkinter as tk
import tk_tools


if __name__ == '__main__':

    root = tk.Tk()

    value = 32766
    blabel1 = tk_tools.BinaryLabel(root, value, "d1:", 16, font="Consolas 12")
    blabel1.grid(row=0, column=0)

    e = tk.Entry(root, width=10)
    e.insert("end", str(value))
    e.grid(row=1, column=0)

    btn_set = tk.Button(root, text="Set",
                        command=lambda: blabel1.set(int(e.get())))
    btn_set.grid(row=1, column=1)

    btn_tmsb = tk.Button(root, text="Toggle MSB", command=blabel1.toggle_msb)
    btn_tmsb.grid(row=1, column=2)

    btn_tlsb = tk.Button(root, text="Toggle LSB", command=blabel1.toggle_lsb)
    btn_tlsb.grid(row=1, column=3)

    root.mainloop()
