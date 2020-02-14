import tkinter as tk
import tk_tools

if __name__ == '__main__':
    root = tk.Tk()

    key_value = tk_tools.KeyValueEntry(
        root, ['key0', 'key1', 'key2'],
        title='help',
        unit_labels=['one', 'two', 'three'],
        defaults=['', 'two', 'three'],
        enables=[True, False, True],
        on_change_callback=lambda: print('works')
    )

    key_value.pack()

    key_value.add_row('key3')
    key_value.add_row('key4', enable=False)
    key_value.add_row('key5', unit_label='five')


    def load_value():
        key_value.load(
            {
                'key0': '1',
                'key1': '2',
                'key2': '3',
                'key3': '4',
                'key4': '5',
                'key5': '6'
            }
        )

    root.after(1000, load_value)
    root.mainloop()
