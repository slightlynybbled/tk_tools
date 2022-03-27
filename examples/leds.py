import tkinter as tk
import tk_tools


def on_click_callback(on):
    if on:
        print('led is on')
    else:
        print('led is off')


if __name__ == '__main__':
    root = tk.Tk()
    root.configure(bg='black')

    led0 = tk_tools.Led(root, size=50, on_click_callback=on_click_callback,
                        bg='black')
    led0.pack()

    tk.Button(root, text='red', command=led0.to_red).pack(fill=tk.X)

    tk.Button(root,
              text='red on',
              command=lambda: led0.to_red(True)).pack(fill=tk.X)

    tk.Button(root, text='green', command=led0.to_green).pack(fill=tk.X)

    tk.Button(root,
              text='green on',
              command=lambda: led0.to_green(True)).pack(fill=tk.X)

    tk.Button(root, text='yellow', command=led0.to_yellow).pack(fill=tk.X)

    tk.Button(root,
              text='yellow on',
              command=lambda: led0.to_yellow(True)).pack(fill=tk.X)

    tk.Button(root, text='grey', command=led0.to_grey).pack(fill=tk.X)

    tk.Label(root, text='Clickable LED').pack(fill=tk.X)

    led1 = tk_tools.Led(root, size=50, on_click_callback=on_click_callback, toggle_on_click=True)
    led1.to_green()
    led1.pack()

    root.mainloop()
