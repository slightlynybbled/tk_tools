import tkinter as tk
import tk_tools


def get_values():
    print('kve0: {}'.format(kve0.get()))
    print('kve1: {}'.format(kve1.get()))
    print('kve2: {}'.format(kve2.get()))


if __name__ == '__main__':

    root = tk.Tk()

    # create the key-value with a title
    kve0 = tk_tools.KeyValueEntry(
        root,
        title='Key/Value 0',
        keys=['Buckets', 'Dollars', 'Hens'],
        unit_labels=['buckets', 'dollars', 'hens'],
    )
    kve0.grid(row=0)

    # create another key-value set without a title and with no units
    kve1 = tk_tools.KeyValueEntry(
        root,
        keys=['Baskets', 'Cows']
    )
    kve1.grid(row=1)

    # create a key-value with some entries disabled, then load values into each
    kve2 = tk_tools.KeyValueEntry(
        root,
        title='Static Key Value',
        keys=['Buckets', 'Dollars', 'Hens'],
        unit_labels=['buckets', 'dollars', 'hens'],
        enables=[False, False, True]
    )
    kve2.grid(row=2)
    kve2.load({'Buckets': 'x', 'Dollars': 'y', 'Hens': 'z'})

    get_values_btn = tk.Button(root, text='Retrieve Values', command=get_values)
    get_values_btn.grid(row=3)

    root.mainloop()
