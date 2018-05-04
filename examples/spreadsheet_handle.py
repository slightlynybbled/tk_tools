import tkinter as tk
import tk_tools


if __name__ == '__main__':

    root = tk.Tk()

    sheet_handle = tk_tools.SpreadSheetReader(root,
                                              path='./ref/test_data.xlsx',
                                              sheetname='Data entry')
    sheet_handle.grid()

    root.mainloop()
