import tkinter
import tk_tools
import locale

# use this as a flag to change the language of the
# calendar using the locale, as shown below
show_in_german = False


def callback():
    print(calendar.selection)


if __name__ == '__main__':

    root = tkinter.Tk()
    root.title('TK Tools Calendar')

    if show_in_german:
        locale.setlocale(locale.LC_ALL, 'deu_deu')

    calendar = tk_tools.Calendar(root)
    calendar.pack()

    calendar.add_callback(callback)

    root.mainloop()
