import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font
import datetime
import calendar
from collections import OrderedDict

import xlrd

try:
    from tk_tools.images import minus
except ImportError:
    minus = ''


class Grid(ttk.Frame):
    padding = 3

    """
    Creates a grid of widgets (intended to be subclassed).

    :param parent: the tk parent element of this frame
    :param num_of_columns: the number of columns contained of the grid
    :param headers: a list containing the names of the column headers
    """
    def __init__(self, parent, num_of_columns: int, headers: list=None,
                 **options):
        self._parent = parent
        super().__init__(self._parent, padding=3, borderwidth=2,
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
                label = ttk.Label(self, text=str(element), relief=tk.GROOVE,
                                  padding=self.padding)
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
    A table-like display widget.

    :param parent: the tk parent element of this frame
    :param num_of_columns: the number of columns contained of the grid
    :param headers: a list containing the names of the column headers
    """
    def __init__(self, parent,
                 num_of_columns: int, headers: list=None,
                 **options):
        self._parent = parent
        super().__init__(self._parent, num_of_columns, headers, **options)

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
            label = ttk.Label(self, text=str(element), relief=tk.GROOVE,
                              padding=self.padding)
            label.grid(row=len(self.rows) + offset, column=i, sticky='E,W')
            row.append(label)

        self.rows.append(row)


class EntryGrid(Grid):
    """
    Add a spreadsheet-like grid of entry widgets.

    :param parent: the tk parent element of this frame
    :param num_of_columns: the number of columns contained of the grid
    :param headers: a list containing the names of the column headers
    """
    def __init__(self, parent,
                 num_of_columns: int, headers: list=None,
                 **options):
        super().__init__(parent, num_of_columns, headers, **options)

    def add_row(self, data: list=None):
        """
        Add a row of data to the current widget, add a <Tab> \
        binding to the last element of the last row, and set \
        the focus at the beginning of the next row.

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
                entry = ttk.Entry(self)
                entry.insert(0, contents)
                entry.grid(row=len(self.rows) + offset, column=i, sticky='E,W')
                row.append(entry)
        else:
            for i in range(self.num_of_columns):
                entry = ttk.Entry(self)
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

        :param as_dicts: True if list of dicts required, else False
        :return: entries as a dict or table
        """
        if as_dicts:
            return self._read_as_dict()
        else:
            return self._read_as_table()


class ButtonGrid(Grid):
    """
    A grid of buttons.

    :param parent: the tk parent element of this frame
    :param num_of_columns: the number of columns contained of the grid
    :param headers: a list containing the names of the column headers
    """
    def __init__(self, parent, num_of_columns: int, headers: list=None,
                 **options):
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
    Creates a key-value input/output frame.

    :param parent: the parent frame
    :param keys: the keys represented
    :param defaults: default values for each key
    :param unit_labels: unit labels for each key (to the right of the value)
    :param enables: True/False for each key
    :param title: The title of the block
    :param on_change_callback: a function callback when any element is changed
    :param options: frame tk options
    """
    def __init__(self, parent, keys: list, defaults: list=None,
                 unit_labels: list=None, enables: list=None,
                 title: str=None, on_change_callback: callable=None,
                 **options):
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
            self.title = ttk.Label(self, text=title)
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

    def add_row(self, key: str, default: str=None,
                unit_label: str=None, enable: bool=None):
        """
        Add a single row and re-draw as necessary

        :param key: the name and dict accessor
        :param default: the default value
        :param unit_label: the label that should be \
        applied at the right of the entry
        :param enable: the 'enabled' state (defaults to True)
        :return:
        """
        self.keys.append(ttk.Label(self, text=key))

        self.defaults.append(default)
        self.unit_labels.append(
            ttk.Label(self, text=unit_label if unit_label else '')
        )
        self.enables.append(enable)
        self.values.append(ttk.Entry(self))

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
        Clears all entries.

        :return: None
        """
        for i in range(len(self.values)):
            self.values[i].delete(0, tk.END)

            if self.defaults[i] is not None:
                self.values[i].insert(0, self.defaults[i])

    def change_enables(self, enables_list: list):
        """
        Enable/disable inputs.

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
        Load values into the key/values via dict.

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
        Retrieve the GUI elements for program use.

        :return: a dictionary containing all \
        of the data from the key/value entries
        """
        data = dict()
        for label, entry in zip(self.keys, self.values):
            data[label.cget('text')] = entry.get()

        return data


class SpreadSheetReader(tk.Frame):
    def __init__(self, parent, path, rows_to_display=20, cols_do_display=8,
                 sheetname=None, **options):
        tk.Frame.__init__(self, parent, **options)

        self.header = ttk.Label(self,
                                text='Select the column you wish to import')
        self.header.grid(row=0, column=0, columnspan=4)

        self.entry_grid = EntryGrid(self, num_of_columns=8)
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


def _get_calendar(locale, fwday):
    # instantiate proper calendar class
    if locale is None:
        return calendar.TextCalendar(fwday)
    else:
        return calendar.LocaleTextCalendar(fwday, locale)


class Calendar(ttk.Frame):
    """
    Graphical date selection widget, with callbacks.

    :param parent: the parent frame
    :param callback: the callable to be executed on selection
    :param kw: tkinter.frame keyword arguments
    """
    timedelta = datetime.timedelta
    datetime = datetime.datetime

    def __init__(self, parent, callback=None, **kwargs):
        # remove custom options from kw before initializing ttk.Frame
        fwday = calendar.SUNDAY
        year = kwargs.pop('year', self.datetime.now().year)
        month = kwargs.pop('month', self.datetime.now().month)
        locale = kwargs.pop('locale', None)
        sel_bg = kwargs.pop('selectbackground', '#ecffc4')
        sel_fg = kwargs.pop('selectforeground', '#05640e')

        self._date = self.datetime(year, month, 1)
        self._selection = None  # no date selected
        self.callback = callback

        super().__init__(parent, **kwargs)

        self._cal = _get_calendar(locale, fwday)

        self.__setup_styles()       # creates custom styles
        self.__place_widgets()      # pack/grid used widgets
        self.__config_calendar()    # adjust calendar columns and setup tags
        # configure a canvas, and proper bindings, for selecting dates
        self.__setup_selection(sel_bg, sel_fg)

        # store items ids, used for insertion later
        self._items = [
            self._calendar.insert('', 'end', values='') for _ in range(6)
        ]

        # insert dates in the currently empty calendar
        self._build_calendar()

    def __setitem__(self, item, value):
        if item in ('year', 'month'):
            raise AttributeError("attribute '%s' is not writeable" % item)
        elif item == 'selectbackground':
            self._canvas['background'] = value
        elif item == 'selectforeground':
            self._canvas.itemconfigure(self._canvas.text, item=value)
        else:
            ttk.Frame.__setitem__(self, item, value)

    def __getitem__(self, item):
        if item in ('year', 'month'):
            return getattr(self._date, item)
        elif item == 'selectbackground':
            return self._canvas['background']
        elif item == 'selectforeground':
            return self._canvas.itemcget(self._canvas.text, 'fill')
        else:
            r = ttk.tclobjs_to_py(
                {item: ttk.Frame.__getitem__(self, item)}
            )
            return r[item]

    def __setup_styles(self):
        # custom ttk styles
        style = ttk.Style(self.master)

        def arrow_layout(dir):
            return [
                ('Button.focus', {
                    'children': [('Button.%sarrow' % dir, None)]
                })
            ]

        style.layout('L.TButton', arrow_layout('left'))
        style.layout('R.TButton', arrow_layout('right'))

    def __place_widgets(self):
        # header frame and its widgets
        hframe = ttk.Frame(self)
        lbtn = ttk.Button(hframe,
                          style='L.TButton',
                          command=self._prev_month)
        rbtn = ttk.Button(hframe,
                          style='R.TButton',
                          command=self._next_month)
        self._header = ttk.Label(hframe, width=15, anchor='center')
        # the calendar
        self._calendar = ttk.Treeview(self, show='',
                                      selectmode='none', height=7)

        # pack the widgets
        hframe.pack(in_=self, side='top', pady=4, anchor='center')
        lbtn.grid(in_=hframe)
        self._header.grid(in_=hframe, column=1, row=0, padx=12)
        rbtn.grid(in_=hframe, column=2, row=0)
        self._calendar.pack(in_=self, expand=1, fill='both', side='bottom')

    def __config_calendar(self):
        cols = self._cal.formatweekheader(3).split()

        self._calendar['columns'] = cols
        self._calendar.tag_configure('header', background='grey90')
        self._calendar.insert('', 'end', values=cols, tag='header')

        # adjust its columns width
        font = Font()
        maxwidth = max(font.measure(col) for col in cols)
        for col in cols:
            self._calendar.column(
                col, width=maxwidth, minwidth=maxwidth, anchor='e'
            )

    def __setup_selection(self, sel_bg, sel_fg):
        self._font = Font()
        self._canvas = canvas = tk.Canvas(
            self._calendar, background=sel_bg,
            borderwidth=0, highlightthickness=0
        )
        canvas.text = canvas.create_text(0, 0, fill=sel_fg, anchor='w')

        canvas.bind('<ButtonPress-1>', lambda evt: canvas.place_forget())
        self._calendar.bind('<Configure>', lambda evt: canvas.place_forget())
        self._calendar.bind('<ButtonPress-1>', self._pressed)

    def __minsize(self, evt):
        width, height = self._calendar.master.geometry().split('x')
        height = height[:height.index('+')]
        self._calendar.master.minsize(width, height)

    def _build_calendar(self):
        year, month = self._date.year, self._date.month

        # update header text (Month, YEAR)
        header = self._cal.formatmonthname(year, month, 0)
        self._header['text'] = header.title()

        # update calendar shown dates
        cal = self._cal.monthdayscalendar(year, month)
        for indx, item in enumerate(self._items):
            week = cal[indx] if indx < len(cal) else []
            fmt_week = [('%02d' % day) if day else '' for day in week]
            self._calendar.item(item, values=fmt_week)

    def _show_selection(self, text, bbox):
        """
        Configure canvas for a new selection.
        """
        x, y, width, height = bbox

        textw = self._font.measure(text)

        canvas = self._canvas
        canvas.configure(width=width, height=height)
        canvas.coords(canvas.text, width - textw, height / 2 - 1)
        canvas.itemconfigure(canvas.text, text=text)
        canvas.place(in_=self._calendar, x=x, y=y)

    # Callbacks

    def _pressed(self, evt):
        """
        Clicked somewhere in the calendar.
        """
        x, y, widget = evt.x, evt.y, evt.widget
        item = widget.identify_row(y)
        column = widget.identify_column(x)

        if not column or not (item in self._items):
            # clicked in the weekdays row or just outside the columns
            return

        item_values = widget.item(item)['values']
        if not len(item_values):  # row is empty for this month
            return

        text = item_values[int(column[1]) - 1]
        if not text:  # date is empty
            return

        bbox = widget.bbox(item, column)
        if not bbox:  # calendar not visible yet
            return

        # update and then show selection
        text = '%02d' % text
        self._selection = (text, item, column)
        self._show_selection(text, bbox)

        if self.callback is not None:
            self.callback()

    def add_callback(self, callback: callable):
        """
        Adds a callback to call when the user clicks on a date

        :param callback: a callable function
        :return: None
        """
        self.callback = callback

    def _prev_month(self):
        """
        Updated calendar to show the previous month.
        """
        self._canvas.place_forget()

        self._date = self._date - self.timedelta(days=1)
        self._date = self.datetime(self._date.year, self._date.month, 1)
        self._build_calendar()  # reconstruct calendar

    def _next_month(self):
        """
        Update calendar to show the next month.
        """
        self._canvas.place_forget()

        year, month = self._date.year, self._date.month
        self._date = self._date + self.timedelta(
            days=calendar.monthrange(year, month)[1] + 1)
        self._date = self.datetime(self._date.year, self._date.month, 1)
        self._build_calendar()  # reconstruct calendar

    @property
    def selection(self):
        """
        Return a datetime representing the current selected date.
        """
        if not self._selection:
            return None

        year, month = self._date.year, self._date.month
        return self.datetime(year, month, int(self._selection[0]))


class _SlotFrame(ttk.Frame):
    """ A single slot """
    def __init__(self, parent, remove_callback=None, entries=1):
        self.parent = parent
        super().__init__(self.parent)

        self.columnconfigure(0, weight=1)
        self._entries = []

        if entries < 1:
            raise ValueError('entries must be >= 1')

        for i in range(entries):
            entry = ttk.Entry(self)
            entry.grid(row=0, column=i, sticky='ew')
            self._entries.append(entry)

        self._image = tk.PhotoImage(data=minus).subsample(2, 2)
        self._remove_btn = ttk.Button(self,
                                      image=self._image, command=self.remove)
        self._remove_btn.grid(row=0, column=entries, sticky='ew')

        self.deleted = False
        self._remove_callback = remove_callback

    def add(self, string: (str, list)):
        """
        Clear the contents of the entry field and
        insert the contents of string.

        :param string: an str containing the text to display
        :return:
        """
        if len(self._entries) == 1:
            self._entries[0].delete(0, 'end')
            self._entries[0].insert(0, string)
        else:
            if len(string) != len(self._entries):
                raise ValueError('the "string" list must be '
                                 'equal to the number of entries')

            for i, e in enumerate(self._entries):
                self._entries[i].delete(0, 'end')
                self._entries[i].insert(0, string[i])

    def remove(self):
        """
        Deletes itself.
        :return: None
        """
        for e in self._entries:
            e.grid_forget()
            e.destroy()

        self._remove_btn.grid_forget()
        self._remove_btn.destroy()

        self.deleted = True

        if self._remove_callback:
            self._remove_callback()

    def get(self):
        """
        Returns the value for the slot.
        :return: the entry value
        """
        values = [e.get() for e in self._entries]
        if len(self._entries) == 1:
            return values[0]
        else:
            return values


class MultiSlotFrame(ttk.Frame):
    """
    Can hold several removable elements,
    such as a list of files, directories,
    or a checklist.::

        # create and grid the frame
        msf = tk_tools.MultiSlotFrame(root)
        msf.grid()

        # add some items
        msf.add('item 1')
        msf.add('item 2')

        # get any user-entered or modified values
        print(msf.get())

    :param parent: the tk parent frame
    :param columns: the number of user columns (defaults to 1)
    """
    def __init__(self, parent, columns=1):
        self._parent = parent
        super().__init__(self._parent)

        self.columnconfigure(0, weight=1)
        self._slot_columns = columns

        self._slots = []

        self._blank_label = None
        self._redraw()

        self._blank_label = ttk.Label(self, text='<no data>')
        self._blank_label.grid(row=0, column=0)

    def _redraw(self):
        """
        Clears the current layout and re-draws all elements in self._slots
        :return:
        """
        if self._blank_label:
            self._blank_label.grid_forget()
            self._blank_label.destroy()
            self._blank_label = None

        for slot in self._slots:
            slot.grid_forget()

        self._slots = [slot for slot in self._slots if not slot.deleted]

        max_per_col = 8
        for i, slot in enumerate(self._slots):
            slot.grid(row=i % max_per_col,
                      column=int(i / max_per_col), sticky='ew')

    def add(self, string: (str, list)):
        """
        Add a new slot to the multi-frame containing the string.
        :param string: a string to insert
        :return: None
        """
        slot = _SlotFrame(self,
                          remove_callback=self._redraw,
                          entries=self._slot_columns)
        slot.add(string)

        self._slots.append(slot)

        self._redraw()

    def clear(self):
        """
        Clear out the multi-frame
        :return:
        """
        for slot in self._slots:
            slot.grid_forget()
            slot.destroy()

        self._slots = []

    def get(self):
        """
        Retrieve and return the values in the multi-frame
        :return: A list of values containing the contents of the GUI
        """
        return [slot.get() for slot in self._slots]
