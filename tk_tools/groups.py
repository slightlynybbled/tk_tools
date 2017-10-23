import tkinter as tk
from collections import OrderedDict

import tk_tools
import xlrd


class Grid(tk.Frame):
    padding = 3

    """
    Creates a grid of widgets (intended to be subclassed)
    """
    def __init__(self, parent, num_of_columns: int, headers: list=None,
                 **options):
        """
        Initialization of the grid object

        :param parent: the tk parent element of this frame
        :param num_of_columns: the number of columns contained of the grid
        :param headers: a list containing the names of the column headers
        """
        tk.Frame.__init__(self, parent, padx=3, pady=3, borderwidth=2,
                          **options)
        self.grid()

        self.headers = list()
        self.rows = list()
        self.num_of_columns = num_of_columns

        # do some validation
        if headers:
            if len(headers) != num_of_columns:
                raise ValueError

            for i, element in enumerate(headers):
                label = tk.Label(self, text=str(element), relief=tk.GROOVE,
                                 padx=self.padding, pady=self.padding)
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

        :return: None
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
    def __init__(self, parent, num_of_columns: int, headers: list=None,
                 **options):
        """
        Initialization of the label grid object

        :param parent: the tk parent element of this frame
        :param num_of_columns: the number of columns contained of the grid
        :param headers: a list containing the names of the column headers
        """
        super().__init__(parent, num_of_columns, headers, **options)

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
            label = tk.Label(self, text=str(element), relief=tk.GROOVE,
                             padx=self.padding, pady=self.padding)
            label.grid(row=len(self.rows) + offset, column=i, sticky='E,W')
            row.append(label)

        self.rows.append(row)


class EntryGrid(Grid):
    """
    Add a spreadsheet-like grid of entry widgets
    """
    def __init__(self, parent, num_of_columns: int, headers: list=None,
                 **options):
        """
        Initialization of the entry grid object

        :param parent: the tk parent element of this frame
        :param num_of_columns: the number of columns contained of the grid
        :param headers: a list containing the names of the column headers
        """
        super().__init__(parent, num_of_columns, headers, **options)

    def add_row(self, data: list=None):
        """
        Add a row of data to the current widget, add a <Tab> binding to the
        last element of the last row, and set the focus at the beginning of
        the next row

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
                contents = '' if element is None else str(element)
                entry = tk.Entry(self)
                entry.insert(0, contents)
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

        :param as_dicts: True if the data is desired as a list of dicts,
        else False
        :return: entries as a dict or table
        """
        if as_dicts:
            return self._read_as_dict()
        else:
            return self._read_as_table()


class ButtonGrid(Grid):
    """
    A grid of buttons.
    """
    def __init__(self, parent, num_of_columns: int, headers: list=None,
                 **options):
        """
        Initialization of the entry grid object

        :param parent: the tk parent element of this frame
        :param num_of_columns: the number of columns contained of the grid
        :param headers: a list containing the names of the column headers
        """
        super().__init__(parent, num_of_columns, headers, **options)

    def add_row(self, data: list = None):
        """
        Add a row of data to the current widget
        :param data: a row of data
        :return: None
        """

        # validation
        if self.headers and data:
            if len(self.headers) != len(data):
                raise ValueError

        offset = 0 if not self.headers else 1
        row = list()

        for i, e in enumerate(data):
            button = tk.Button(self, text=str(e[0]), relief=tk.RAISED,
                               command=e[1], padx=self.padding,
                               pady=self.padding)

            button.grid(row=len(self.rows) + offset, column=i, sticky='E,W')
            row.append(button)

        self.rows.append(row)


class KeyValueEntry(tk.Frame):
    """
    Creates a key-value frame so common in modern GUI
    """
    def __init__(self, parent, keys: list, defaults: list=None,
                 unit_labels: list=None, enables: list=None,
                 title=None, on_change_callback=None, **options):
        """
        Key/Value constructor

        :param parent: the parent frame
        :param keys: the keys represented
        :param defaults: default values for each key
        :param unit_labels: unit labels for each key
        (to the right of the value)
        :param enables: True/False for each key
        :param title: The title of the block
        :param on_change_callback: a function callback when any element
        is changed
        :param options: frame tk options
        """
        tk.Frame.__init__(self, parent,
                          borderwidth=2,
                          padx=5, pady=5,
                          **options)

        # some checks before proceeding
        if defaults:
            if len(keys) != len(defaults):
                raise ValueError('unit_labels length does not '
                                 'match keys length')
        if unit_labels:
            if len(keys) != len(unit_labels):
                raise ValueError('unit_labels length does not '
                                 'match keys length')
        if enables:
            if len(keys) != len(enables):
                raise ValueError('enables length does not '
                                 'match keys length')

        self.keys = []
        self.values = []
        self.defaults = []
        self.unit_labels = []
        self.enables = []
        self.callback = on_change_callback

        if title is not None:
            self.title = tk.Label(self, text=title)
            self.title.grid(row=0, column=0, columnspan=3)
        else:
            self.title = None

        for i in range(len(keys)):
            self.add_row(
                key=keys[i],
                default=defaults[i] if defaults else None,
                unit_label=unit_labels[i] if unit_labels else None,
                enable=enables[i] if enables else None
            )

    def add_row(self, key, default=None, unit_label=None, enable=None):
        """
        Add a single row and re-draw as necessary

        :param key: the name and dict accessor
        :param default: the default value
        :param unit_label: the label that should be
        applied at the right of the entry
        :param enable: the 'enabled' state (defaults to true)
        :return:
        """
        self.keys.append(tk.Label(self, text=key))

        self.defaults.append(default)
        self.unit_labels.append(
            tk.Label(self, text=unit_label if unit_label else '')
        )
        self.enables.append(enable)
        self.values.append(tk.Entry(self))

        row_offset = 1 if self.title is not None else 0

        for i in range(len(self.keys)):
            self.keys[i].grid_forget()

            self.keys[i].grid(row=row_offset, column=0, sticky='e')
            self.values[i].grid(row=row_offset, column=1)

            if self.unit_labels[i]:
                self.unit_labels[i].grid(row=row_offset, column=3, sticky='w')

            if self.defaults[i]:
                self.values[i].config(state=tk.NORMAL)
                self.values[i].delete(0, tk.END)
                self.values[i].insert(0, self.defaults[i])

            if self.enables[i] in [True, None]:
                self.values[i].config(state=tk.NORMAL)
            elif self.enables[i] is False:
                self.values[i].config(state=tk.DISABLED)

            row_offset += 1

            # strip <Return> and <Tab> bindings, add callbacks to all entries
            self.values[i].unbind('<Return>')
            self.values[i].unbind('<Tab>')

            if self.callback is not None:
                def callback(event):
                    self.callback()

                self.values[i].bind('<Return>', callback)
                self.values[i].bind('<Tab>', callback)

    def reset(self):
        """
        Clears all entries

        :return: None
        """
        for i in range(len(self.values)):
            self.values[i].delete(0, tk.END)

            if self.defaults[i] is not None:
                self.values[i].insert(0, self.defaults[i])

    def change_enables(self, enables_list: list):
        """
        Enable/disable inputs

        :param enables_list: list containing enables for each key
        :return: None
        """
        for i, entry in enumerate(self.values):
            if enables_list[i]:
                entry.config(state=tk.NORMAL)
            else:
                entry.config(state=tk.DISABLED)

    def load(self, data: dict):
        """
        Load values into the key/values via dict
        :param data: dict containing the key/values that should be inserted
        :return: None
        """
        for i, label in enumerate(self.keys):
            key = label.cget('text')
            if key in data.keys():
                entry_was_enabled = True if \
                    self.values[i].cget('state') == 'normal' else False
                if not entry_was_enabled:
                    self.values[i].config(state='normal')

                self.values[i].delete(0, tk.END)
                self.values[i].insert(0, str(data[key]))

                if not entry_was_enabled:
                    self.values[i].config(state='disabled')

    def get(self):
        """
        Retrieve the GUI elements for program use
        :return: a dictionary containing all of the
        data from the key/value entries
        """
        data = dict()
        for label, entry in zip(self.keys, self.values):
            data[label.cget('text')] = entry.get()

        return data


class SpreadSheetReader(tk.Frame):
    def __init__(self, parent, path, rows_to_display=20, cols_do_display=8,
                 sheetname=None, **options):
        tk.Frame.__init__(self, parent, **options)

        self.header = tk.Label(self,
                               text='Select the column you wish to import')
        self.header.grid(row=0, column=0, columnspan=4)

        self.entry_grid = tk_tools.EntryGrid(self, num_of_columns=8)
        self.entry_grid.grid(row=1, column=0, columnspan=4, rowspan=4)

        self.move_page_up_btn = tk.Button(self, text='^\n^',
                                          command=lambda: self.move_up(
                                              page=True)
                                          )
        self.move_page_up_btn.grid(row=1, column=4, sticky='NS')
        self.move_page_up_btn = tk.Button(self, text='^',
                                          command=self.move_up)
        self.move_page_up_btn.grid(row=2, column=4, sticky='NS')

        self.move_page_down_btn = tk.Button(self, text='v',
                                            command=self.move_down)
        self.move_page_down_btn.grid(row=3, column=4, sticky='NS')
        self.move_page_down_btn = tk.Button(self, text='v\nv',
                                            command=lambda: self.move_down(
                                                page=True)
                                            )
        self.move_page_down_btn.grid(row=4, column=4, sticky='NS')

        # add buttons to navigate the spreadsheet
        self.move_page_left_btn = tk.Button(self, text='<<',
                                            command=lambda: self.move_left(
                                                page=True)
                                            )
        self.move_page_left_btn.grid(row=5, column=0, sticky='EW')
        self.move_left_btn = tk.Button(self, text='<', command=self.move_left)
        self.move_left_btn.grid(row=5, column=1, sticky='EW')
        self.move_right_btn = tk.Button(self,
                                        text='>',
                                        command=self.move_right)
        self.move_right_btn.grid(row=5, column=2, sticky='EW')
        self.move_page_right_btn = tk.Button(self,
                                             text='>>',
                                             command=lambda: self.move_right(
                                                 page=True)
                                             )
        self.move_page_right_btn.grid(row=5, column=3, sticky='EW')

        self.path = path
        self.sheetname = sheetname
        self.rows_to_display = rows_to_display
        self.cols_to_display = cols_do_display
        self.current_position = (0, 0)

        self.read_xl(sheetname=self.sheetname)

    def read_xl(self, row_number=0, column_number=0,
                sheetname=None, sheetnum=0):
        workbook = xlrd.open_workbook(self.path)

        if sheetname:
            sheet = workbook.sheet_by_name(sheetname)
        else:
            sheet = workbook.sheet_by_index(sheetnum)

        for i, row in enumerate(sheet.get_rows()):
            if i >= row_number:
                data = row[column_number:column_number + self.cols_to_display]
                data = [point.value for point in data]
                self.entry_grid.add_row(data=data)

            if i >= (self.rows_to_display + row_number):
                break

    def move_right(self, page=False):
        row_pos, col_pos = self.current_position
        self.entry_grid.clear()

        if page:
            self.current_position = (row_pos, col_pos + self.cols_to_display)
        else:
            self.current_position = (row_pos, col_pos + 1)
        self.read_xl(*self.current_position, sheetname=self.sheetname)

    def move_left(self, page=False):
        row_pos, col_pos = self.current_position

        if not page and col_pos == 0:
            return

        if page and col_pos < self.cols_to_display:
            return

        self.entry_grid.clear()

        if page:
            self.current_position = (row_pos, col_pos - self.cols_to_display)
        else:
            self.current_position = (row_pos, col_pos - 1)
        self.read_xl(*self.current_position, sheetname=self.sheetname)

    def move_down(self, page=False):
        row_pos, col_pos = self.current_position
        self.entry_grid.clear()

        if page:
            self.current_position = (row_pos + self.rows_to_display, col_pos)
        else:
            self.current_position = (row_pos + 1, col_pos)
        self.read_xl(*self.current_position, sheetname=self.sheetname)

    def move_up(self, page=False):
        row_pos, col_pos = self.current_position

        if not page and row_pos == 0:
            return

        if page and row_pos < self.rows_to_display:
            return

        self.entry_grid.clear()

        if page:
            self.current_position = (row_pos - self.rows_to_display, col_pos)
        else:
            self.current_position = (row_pos - 1, col_pos)
        self.read_xl(*self.current_position, sheetname=self.sheetname)


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
        print(entry_grid.read(as_dicts=False))

    read_btn = tk.Button(text='Read', command=read)
    read_btn.grid(row=3, column=0)

    root.mainloop()
