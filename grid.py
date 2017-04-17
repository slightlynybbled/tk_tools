import tkinter as tk
from collections import OrderedDict


class Grid(tk.Frame):
    """
    Creates a grid of widgets (intended to be subclassed)
    """
    def __init__(self, parent, num_of_columns: int, headers: list=None):
        """
        Initialization of the grid object
        
        :param parent: the tk parent element of this frame
        :param num_of_columns: the number of columns contained of the grid
        :param headers: a list containing the names of the column headers
        """
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
        """
        Adds a row of data based on the entered data
        
        :param data: row of data as a list
        :return: None
        """
        raise NotImplementedError

    def _redraw(self):
        """
        Forgets the current layout and redraws with the most recent information
        
        :return: 
        """
        for row in self.rows:
            for widget in row:
                widget.grid_forget()

        offset = 0 if not self.headers else 1
        for i, row in enumerate(self.rows):
            for j, widget in enumerate(row):
                widget.grid(row=i+offset, column=j)

    def remove_row(self, row_number: int=-1):
        """
        Removes a specified row of data
        
        :param row_number: the row to remove (defaults to the last row)
        :return: None
        """
        if len(self.rows) == 0:
            return

        row = self.rows.pop(row_number)
        for widget in row:
            widget.destroy()

    def clear(self):
        """
        Removes all elements of the grid
        
        :return: None 
        """
        for i in range(len(self.rows)):
            self.remove_row(0)


class LabelGrid(Grid):
    """
    A table-like display widget
    """
    def __init__(self, parent, num_of_columns: int, headers: list=None):
        """
        Initialization of the label grid object

        :param parent: the tk parent element of this frame
        :param num_of_columns: the number of columns contained of the grid
        :param headers: a list containing the names of the column headers
        """
        super().__init__(parent, num_of_columns, headers)

    def add_row(self, data: list):
        """
        Add a row of data to the current widget
        
        :param data: a row of data
        :return: None
        """
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
    """
    Add a spreadsheet-like grid of entry widgets
    """
    def __init__(self, parent, num_of_columns: int, headers: list=None):
        """
        Initialization of the entry grid object

        :param parent: the tk parent element of this frame
        :param num_of_columns: the number of columns contained of the grid
        :param headers: a list containing the names of the column headers
        """
        super().__init__(parent, num_of_columns, headers)

    def add_row(self, data: list=None):
        """
        Add a row of data to the current widget, add a <Tab> binding to the 
        last element of the last row, and set the focus at the beginning of the next row

        :param data: a row of data
        :return: None
        """
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
        """
        Read the data contained in all entries as a list of 
        dictionaries with the headers as the dictionary keys
        
        :return: list of dicts containing all tabular data 
        """
        data = list()
        for row in self.rows:
            row_data = OrderedDict()
            for i, header in enumerate(self.headers):
                row_data[header.cget('text')] = row[i].get()

            data.append(row_data)

        return data

    def _read_as_table(self):
        """
        Read the data contained in all entries as a list of 
        lists containing all of the data

        :return: list of dicts containing all tabular data 
        """
        rows = list()

        for row in self.rows:
            rows.append([row[i].get() for i in range(self.num_of_columns)])

        return rows

    def read(self, as_dicts=True):
        """
        Read the data from the entry fields
        
        :param as_dicts: True if the data is desired as a list of dicts, else False
        :return: 
        """
        if as_dicts:
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
