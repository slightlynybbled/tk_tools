import tkinter
from tk_tools import Calendar

root = tkinter.Tk()
root.title('TK Tools Calendar')
cal = Calendar()
cal.pack(expand=1, fill='both')


def custom_callback():
    print(cal.selection)


cal.add_callback(custom_callback)

root.mainloop()