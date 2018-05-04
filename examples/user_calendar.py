import tkinter
import tk_tools


def callback():
    print(calendar.selection)


if __name__ == '__main__':

    root = tkinter.Tk()
    root.title('TK Tools Calendar')
    calendar = tk_tools.Calendar(root)
    calendar.pack()

    calendar.add_callback(callback)

    root.mainloop()
