import tkinter as tk
import tk_tools

root = tk.Tk()

handle = tk_tools.SpreadSheetReader(root,
                                    path='./ref/test_data.xlsx',
                                    sheetname='Data entry')
handle.grid()

root.mainloop()
