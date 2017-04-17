import tkinter as tk
from collections import OrderedDict


class Grid(tk.Frame):
    def __init__(self, parent, num_of_columns: int, headers: list=None):
        tk.Frame.__init__(self, parent, padx=3, pady=3, borderwidth=2)
        self.grid()

        self.headers = list()
        self.rows = list()
        self.num_of_columns = num_of_columns

        # do some validation
        if headers:
            if len(headers) != num_of_columns:
                raise ValueError

            for i, element in enumerate(headers):
                label = tk.Label(self, text=str(element), relief=tk.GROOVE)
                label.grid(row=0, column=i, sticky='E,W')
                self.headers.append(label)

    def add_row(self, data: list):
        raise NotImplementedError

    def _redraw(self):
        for row in self.rows:
            for widget in row:
                widget.grid_forget()

        offset = 0 if not self.headers else 1
        for i, row in enumerate(self.rows):
            for j, widget in enumerate(row):
                widget.grid(row=i+offset, column=j)

    def remove_row(self, row_number: int):
        if len(self.rows) == 0:
            return

        row = self.rows.pop(row_number)
        for widget in row:
            widget.destroy()

    def clear(self):
        for i in range(len(self.rows)):
            self.remove_row(0)


class LabelGrid(Grid):
    def __init__(self, parent, num_of_columns: int, headers: list=None):
        super().__init__(parent, num_of_columns, headers)

    def add_row(self, data: list):
        # validation
        if self.headers:
            if len(self.headers) != len(data):
                raise ValueError

        offset = 0 if not self.headers else 1
        row = list()
        for i, element in enumerate(data):
            label = tk.Label(self, text=str(element), relief=tk.GROOVE)
            label.grid(row=len(self.rows) + offset, column=i, sticky='E,W')
            row.append(label)


class EntryGrid(Grid):
    def __init__(self, parent, num_of_columns: int, headers: list=None):
        super().__init__(parent, num_of_columns, headers)

    def add_row(self, data: list=None):
        # validation
        if self.headers and data:
            if len(self.headers) != len(data):
                raise ValueError

        offset = 0 if not self.headers else 1
        row = list()

        if data:
            for i, element in enumerate(data):
                contents = '' if element is not None else str(element)
                entry = tk.Entry(self, text=contents)
                entry.grid(row=len(self.rows) + offset, column=i, sticky='E,W')
                row.append(entry)
        else:
            for i in range(self.num_of_columns):
                entry = tk.Entry(self)
                entry.grid(row=len(self.rows) + offset, column=i, sticky='E,W')
                row.append(entry)

        self.rows.append(row)

        # clear all bindings
        for row in self.rows:
            for widget in row:
                widget.unbind('<Tab>')

        def add(e):
            self.add_row()

        last_entry = self.rows[-1][-1]
        last_entry.bind('<Tab>', add)

        e = self.rows[-1][0]
        e.focus_set()

        self._redraw()

    def _read_as_dict(self):
        data = list()
        for row in self.rows:
            row_data = OrderedDict()
            for i, header in enumerate(self.headers):
                row_data[header.cget('text')] = row[i].get()

            data.append(row_data)

        return data

    def _read_as_table(self):
        rows = list()

        for row in self.rows:
            rows.append([row[i].get() for i in range(self.num_of_columns)])

        return rows

    def read(self, as_dict=True):
        if as_dict:
            return self._read_as_dict()
        else:
            return self._read_as_table()


if __name__ == '__main__':
    root = tk.Tk()

    entry_grid = EntryGrid(root, 3, ['L0', 'L1', 'L2'])
    entry_grid.grid(row=0, column=0)

    def add_row():
        row = [1, 2, 3]
        entry_grid.add_row(row)

    add_row_btn = tk.Button(text='Add Row', command=add_row)
    add_row_btn.grid(row=1, column=0)

    def remove_row():
        entry_grid.remove_row(0)

    remove_row_btn = tk.Button(text='Remove Row', command=remove_row)
    remove_row_btn.grid(row=2, column=0)

    def read():
        print(entry_grid.read(as_dict=False))

    read_btn = tk.Button(text='Read', command=read)
    read_btn.grid(row=3, column=0)


    root.mainloop()
