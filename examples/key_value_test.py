import tkinter as tk
import tk_tools

root = tk.Tk()

kv = tk_tools.KeyValueEntry(
    root, ['key0', 'key1', 'key2'],
    title='help',
    unit_labels=['one', 'two', 'three'],
    defaults=['', 'two', 'three'],
    enables=[True, False, True],
    on_change_callback=lambda: print('works')
)
kv.pack()

kv.add_row('key3')
kv.add_row('key4', enable=False)
kv.add_row('key5', unit_label='five')

kv.load(
    {
        'key0': '1',
        'key1': '2',
        'key2': '3',
        'key3': '4',
        'key4': '5',
        'key5': '6'
    }
)

root.mainloop()
