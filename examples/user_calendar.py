import tkinter
import tk_tools

root = tkinter.Tk()
root.title('TK Tools Calendar')
cal = tk_tools.Calendar(root)
cal.pack()


def custom_callback():
    print(cal.selection)


cal.add_callback(custom_callback)

root.mainloop()
