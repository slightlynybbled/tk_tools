import tkinter as tk
import tkinter.ttk as ttk
import cmath
import sys
import logging
from decimal import Decimal

# these imports make autodoc easier to run
try:
    from engineering_notation import EngNumber
except ImportError:
    pass

try:
    from tk_tools.images import rotary_scale, \
        led_green, led_green_on, led_yellow, led_yellow_on, \
        led_red, led_red_on, led_grey
except ImportError:
    pass

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if getattr(sys, 'frozen', False):
    frozen = True
else:
    frozen = False

logger.info('frozen: {}'.format(frozen))


class Dial(ttk.Frame):
    """
    Base class for all dials and dial-like widgets
    """
    def __init__(self, parent, size=100, **options):
        self._parent = parent
        super().__init__(self._parent, padding=3, borderwidth=2, **options)

        self.size = size

    def to_absolute(self, x, y):
        """
        Converts coordinates provided with reference to the center \
        of the canvas (0, 0) to absolute coordinates which are used \
        by the canvas object in which (0, 0) is located in the top \
        left of the object.

        :param x: x value in pixels
        :param y: x value in pixels
        :return: None
        """
        return x + self.size/2, y + self.size/2


class Compass(Dial):
    """
    Displays a compass typically seen on a map
    """
    def __init__(self, parent, size=100, **options):
        super().__init__(parent, size=size, **options)
        raise NotImplementedError()

        # todo: import an image, place the image on the canvas, then place
        # an arrow on top of the image


class RotaryScale(Dial):
    """
    Shows a rotary scale, much like a speedometer.::

        rs = tk_tools.RotaryScale(root, max_value=100.0, size=100, unit='km/h')
        rs.grid(row=0, column=0)

        rs.set_value(10)

    :param parent: tkinter parent frame
    :param max_value: the value corresponding to the maximum value on the scale
    :param size: the size in pixels
    :param options: the frame options
    """
    def __init__(self, parent,
                 max_value: (float, int)=100.0, size: (float, int)=100,
                 unit: str=None, img_data: str=None,
                 needle_color='blue', needle_thickness=0,
                 **options):
        super().__init__(parent, size=size, **options)

        self.max_value = float(max_value)
        self.size = size
        self.unit = '' if not unit else unit
        self.needle_color = needle_color
        self.needle_thickness = needle_thickness

        self.canvas = tk.Canvas(self, width=self.size, height=self.size)
        self.canvas.grid(row=0)
        self.readout = tk.Label(self, text='-{}'.format(self.unit))
        self.readout.grid(row=1)

        if img_data:
            self.image = tk.PhotoImage(data=img_data)
        else:
            self.image = tk.PhotoImage(data=rotary_scale)

        self.image = self.image.subsample(int(200 / self.size),
                                          int(200 / self.size))

        initial_value = 0.0
        self.set_value(initial_value)

    def set_value(self, number: (float, int)):
        """
        Sets the value of the graphic

        :param number: the number (must be between 0 and \
        'max_range' or the scale will peg the limits
        :return: None
        """
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, image=self.image, anchor='nw')

        number = number if number <= self.max_value else self.max_value
        number = 0.0 if number < 0.0 else number

        radius = 0.9 * self.size/2.0
        angle_in_radians = (2.0 * cmath.pi / 3.0) \
            + number / self.max_value * (5.0 * cmath.pi / 3.0)

        center = cmath.rect(0, 0)
        outer = cmath.rect(radius, angle_in_radians)
        if self.needle_thickness == 0:
            line_width = int(5 * self.size / 200)
            line_width = 1 if line_width < 1 else line_width
        else:
            line_width = self.needle_thickness

        self.canvas.create_line(
            *self.to_absolute(center.real, center.imag),
            *self.to_absolute(outer.real, outer.imag),
            width=line_width,
            fill=self.needle_color
        )

        self.readout['text'] = '{}{}'.format(number, self.unit)

    def _draw_background(self, divisions=10):
        """
        Draws the background of the dial

        :param divisions: the number of divisions
        between 'ticks' shown on the dial
        :return: None
        """
        self.canvas.create_arc(2, 2, self.size-2, self.size-2,
                               style=tk.PIESLICE, start=-60, extent=30,
                               fill='red')
        self.canvas.create_arc(2, 2, self.size-2, self.size-2,
                               style=tk.PIESLICE, start=-30, extent=60,
                               fill='yellow')
        self.canvas.create_arc(2, 2, self.size-2, self.size-2,
                               style=tk.PIESLICE, start=30, extent=210,
                               fill='green')

        # find the distance between the center and the inner tick radius
        inner_tick_radius = int(self.size * 0.4)
        outer_tick_radius = int(self.size * 0.5)

        for tick in range(divisions):
            angle_in_radians = (2.0 * cmath.pi / 3.0) \
                               + tick/divisions * (5.0 * cmath.pi / 3.0)
            inner_point = cmath.rect(inner_tick_radius, angle_in_radians)
            outer_point = cmath.rect(outer_tick_radius, angle_in_radians)

            self.canvas.create_line(
                *self.to_absolute(inner_point.real, inner_point.imag),
                *self.to_absolute(outer_point.real, outer_point.imag),
                width=1
            )


class Gauge(ttk.Frame):
    """
    Shows a gauge, much like the RotaryGauge.::

        gauge = tk_tools.Gauge(root, max_value=100.0,
                               label='speed', unit='km/h')
        gauge.grid()
        gauge.set_value(10)

    :param parent: tkinter parent frame
    :param width: canvas width
    :param height: canvas height
    :param min_value: the minimum value
    :param max_value: the maximum value
    :param label: the label on the scale
    :param unit: the unit to show on the scale
    :param divisions: the number of divisions on the scale
    :param yellow: the beginning of the yellow (warning) zone in percent
    :param red: the beginning of the red (danger) zone in percent
    :param yellow_low: in percent warning for low values
    :param red_low: in percent if very low values are a danger
    :param bg: background
    """
    def __init__(self, parent, width=200, height=100,
                 min_value=0.0, max_value=100.0, label='', unit='',
                 divisions=8, yellow=50, red=80, yellow_low=0,
                 red_low=0, bg='lightgrey'):
        self._parent = parent
        self._width = width
        self._height = height
        self._label = label
        self._unit = unit
        self._divisions = divisions
        self._min_value = EngNumber(min_value)
        self._max_value = EngNumber(max_value)
        self._average_value = EngNumber((max_value + min_value) / 2)
        self._yellow = yellow * 0.01
        self._red = red * 0.01
        self._yellow_low = yellow_low * 0.01
        self._red_low = red_low * 0.01

        super().__init__(self._parent)

        self._canvas = tk.Canvas(self, width=self._width,
                                 height=self._height, bg=bg)
        self._canvas.grid(row=0, column=0, sticky='news')
        self._min_value = EngNumber(min_value)
        self._max_value = EngNumber(max_value)
        self._value = self._min_value
        self._redraw()

    def _redraw(self):
        self._canvas.delete('all')
        max_angle = 120.0
        value_as_percent = ((self._value - self._min_value) /
                            (self._max_value - self._min_value))
        value = float(max_angle * value_as_percent)
        # no int() => accuracy
        # create the tick marks and colors across the top
        for i in range(self._divisions):
            extent = (max_angle / self._divisions)
            start = (150.0 - i * extent)
            rate = (i+1)/(self._divisions+1)
            if rate < self._red_low:
                bg_color = 'red'
            elif rate <= self._yellow_low:
                bg_color = 'yellow'
            elif rate <= self._yellow:
                bg_color = 'green'
            elif rate <= self._red:
                bg_color = 'yellow'
            else:
                bg_color = 'red'

            self._canvas.create_arc(
                0, int(self._height * 0.15),
                self._width, int(self._height * 1.8),
                start=start, extent=-extent, width=2,
                fill=bg_color, style='pie'
            )
        bg_color = 'white'
        red = '#c21807'
        ratio = 0.06
        self._canvas.create_arc(self._width * ratio,
                                int(self._height * 0.25),
                                self._width * (1.0 - ratio),
                                int(self._height * 1.8 * (1.0 - ratio * 1.1)),
                                start=150, extent=-120, width=2,
                                fill=bg_color, style='pie')
        # readout & title
        self.readout(self._value, 'black')  # BG black if OK

        # display lowest value
        value_text = '{}'.format(self._min_value)
        self._canvas.create_text(
            self._width * 0.1, self._height * 0.7,
            font=('Courier New', 10), text=value_text)
        # display greatest value
        value_text = '{}'.format(self._max_value)
        self._canvas.create_text(
            self._width * 0.9, self._height * 0.7,
            font=('Courier New', 10), text=value_text)
        # display center value
        value_text = '{}'.format(self._average_value)
        self._canvas.create_text(
            self._width * 0.5, self._height * 0.1,
            font=('Courier New', 10), text=value_text)
        # create first half (red needle)
        self._canvas.create_arc(0, int(self._height * 0.15),
                                self._width, int(self._height * 1.8),
                                start=150, extent=-value, width=3,
                                outline=red)

        # create inset red
        self._canvas.create_arc(self._width * 0.35, int(self._height * 0.75),
                                self._width * 0.65, int(self._height * 1.2),
                                start=150, extent=-120, width=1,
                                outline='grey', fill=red, style='pie')

        # create the overlapping border
        self._canvas.create_arc(0, int(self._height * 0.15),
                                self._width, int(self._height * 1.8),
                                start=150, extent=-120, width=4,
                                outline='#343434')

    def readout(self, value, bg):  # value, BG color
        # draw the black behind the readout
        r_width = 95
        r_height = 20
        r_offset = 8
        self._canvas.create_rectangle(
            self._width/2.0 - r_width / 2.0,
            self._height/2.0 - r_height/2.0 + r_offset,
            self._width/2.0 + r_width / 2.0,
            self._height/2.0 + r_height/2.0 + r_offset,
            fill=bg, outline='grey'
        )
        # the digital readout
        self._canvas.create_text(
            self._width * 0.5, self._height * 0.5 - r_offset,
            font=('Courier New', 10), text=self._label)

        value_text = '{}{}'.format(self._value, self._unit)
        self._canvas.create_text(
            self._width * 0.5, self._height * 0.5 + r_offset,
            font=('Courier New', 10), text=value_text, fill='white')

    def set_value(self, value):
        self._value = EngNumber(value)
        if self._min_value * 1.02 < value < self._max_value * 0.98:
            self._redraw()      # refresh all
        else:                   # OFF limits refresh only readout
            self.readout(self._value, 'red')  # on RED BackGround


class Graph(ttk.Frame):
    """
    Tkinter native graph (pretty basic, but doesn't require heavy install).::

        graph = tk_tools.Graph(
            parent=root,
            x_min=-1.0,
            x_max=1.0,
            y_min=0.0,
            y_max=2.0,
            x_tick=0.2,
            y_tick=0.2,
            width=500,
            height=400
        )

        graph.grid(row=0, column=0)

        # create an initial line
        line_0 = [(x/10, x/10) for x in range(10)]
        graph.plot_line(line_0)

    :param parent: the parent frame
    :param x_min: the x minimum
    :param x_max: the x maximum
    :param y_min: the y minimum
    :param y_max: the y maximum
    :param x_tick: the 'tick' on the x-axis
    :param y_tick: the 'tick' on the y-axis
    :param options: additional valid tkinter.canvas options
    """
    def __init__(self, parent, x_min: float, x_max: float,
                 y_min: float, y_max: float,
                 x_tick: float, y_tick: float,
                 **options):
        self._parent = parent
        super().__init__(self._parent, **options)

        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0)

        self.w = float(self.canvas.config('width')[4])
        self.h = float(self.canvas.config('height')[4])
        self.x_min = x_min
        self.x_max = x_max
        self.x_tick = x_tick
        self.y_min = y_min
        self.y_max = y_max
        self.y_tick = y_tick
        self.px_x = (self.w - 100) / ((x_max - x_min) / x_tick)
        self.px_y = (self.h - 100) / ((y_max - y_min) / y_tick)

        self.draw_axes()

    def draw_axes(self):
        """
        Removes all existing series and re-draws the axes.

        :return: None
        """
        self.canvas.delete('all')
        rect = 50, 50, self.w - 50, self.h - 50

        self.canvas.create_rectangle(rect, outline="black")

        for x in self.frange(0, self.x_max - self.x_min + 1, self.x_tick):
            value = Decimal(self.x_min + x)
            if self.x_min <= value <= self.x_max:
                x_step = (self.px_x * x) / self.x_tick
                coord = 50 + x_step, self.h - 50, 50 + x_step, self.h - 45
                self.canvas.create_line(coord, fill="black")
                coord = 50 + x_step, self.h - 40

                label = round(Decimal(self.x_min + x), 1)
                self.canvas.create_text(coord, fill="black", text=label)

        for y in self.frange(0, self.y_max - self.y_min + 1, self.y_tick):
            value = Decimal(self.y_max - y)

            if self.y_min <= value <= self.y_max:
                y_step = (self.px_y * y) / self.y_tick
                coord = 45, 50 + y_step, 50, 50 + y_step
                self.canvas.create_line(coord, fill="black")
                coord = 35, 50 + y_step

                label = round(value, 1)
                self.canvas.create_text(coord, fill="black", text=label)

    def plot_point(self, x, y, visible=True, color='black', size=5):
        """
        Places a single point on the grid

        :param x: the x coordinate
        :param y: the y coordinate
        :param visible: True if the individual point should be visible
        :param color: the color of the point
        :param size: the point size in pixels
        :return: The absolute coordinates as a tuple
        """
        xp = (self.px_x * (x - self.x_min)) / self.x_tick
        yp = (self.px_y * (self.y_max - y)) / self.y_tick
        coord = 50 + xp, 50 + yp

        if visible:
            # divide down to an appropriate size
            size = int(size/2) if int(size/2) > 1 else 1
            x, y = coord

            self.canvas.create_oval(
                x-size, y-size,
                x+size, y+size,
                fill=color
            )

        return coord

    def plot_line(self, points: list, color='black', point_visibility=False):
        """
        Plot a line of points

        :param points: a list of tuples, each tuple containing an (x, y) point
        :param color: the color of the line
        :param point_visibility: True if the points \
        should be individually visible
        :return: None
        """
        last_point = ()
        for point in points:
            this_point = self.plot_point(point[0], point[1],
                                         color=color, visible=point_visibility)

            if last_point:
                self.canvas.create_line(last_point + this_point, fill=color)
            last_point = this_point
            # print last_point

    @staticmethod
    def frange(start, stop, step, digits_to_round=3):
        """
        Works like range for doubles

        :param start: starting value
        :param stop: ending value
        :param step: the increment_value
        :param digits_to_round: the digits to which to round \
        (makes floating-point numbers much easier to work with)
        :return: generator
        """
        while start < stop:
            yield round(start, digits_to_round)
            start += step


class Led(ttk.Frame):
    """
    Create an LED-like interface for the user.::

        led = tk_tools.Led(root, size=50)
        led.pack()

        led.to_red()
        led.to_green(on=True)

    The user also has the option of adding an `on_click_callback`
    function.  When the button is clicked, the button will change
    state and the on-click callback will be executed.  The
    callback must accept a single boolean parameter, `on`, which
    indicates if the LED was just turned on or off.

    :param parent: the parent frame
    :param size: the size in pixels
    :param on_click_callback: a callback which accepts a boolean parameter 'on'
    :param options: the frame options
    """
    def __init__(self, parent, size=100,
                 on_click_callback=None, toggle_on_click=False, **options):
        self._parent = parent
        super().__init__(self._parent, padding=3, borderwidth=2,
                         **options)

        self._size = size

        self._canvas = tk.Canvas(self, width=self._size, height=self._size)
        self._canvas.grid(row=0)
        self._image = None
        self._on = False
        self._user_click_callback = on_click_callback
        self._toggle_on_click = toggle_on_click

        self.to_grey()

        def on_click(e):
            if self._user_click_callback is not None:
                self._user_click_callback(self._on)

        self._canvas.bind('<Button-1>', on_click)

    def _load_new(self, img_data: str):
        """
        Load a new image.

        :param img_data: the image data as a base64 string
        :return: None
        """
        self._image = tk.PhotoImage(data=img_data)
        self._image = self._image.subsample(int(200 / self._size),
                                            int(200 / self._size))
        self._canvas.delete('all')
        self._canvas.create_image(0, 0, image=self._image, anchor='nw')

        if self._user_click_callback is not None:
            self._user_click_callback(self._on)

    def to_grey(self, on: bool=False):
        """
        Change the LED to grey.

        :param on: Unused, here for API consistency with the other states
        :return: None
        """
        self._on = False
        self._load_new(led_grey)

    def to_green(self, on: bool=False):
        """
        Change the LED to green (on or off).

        :param on: True or False
        :return: None
        """
        self._on = on
        if on:
            self._load_new(led_green_on)

            if self._toggle_on_click:
                self._canvas.bind('<Button-1>', lambda x: self.to_green(False))
        else:
            self._load_new(led_green)

            if self._toggle_on_click:
                self._canvas.bind('<Button-1>', lambda x: self.to_green(True))

    def to_red(self, on: bool=False):
        """
        Change the LED to red (on or off)
        :param on: True or False
        :return: None
        """
        self._on = on
        if on:
            self._load_new(led_red_on)

            if self._toggle_on_click:
                self._canvas.bind('<Button-1>', lambda x: self.to_red(False))
        else:
            self._load_new(led_red)

            if self._toggle_on_click:
                self._canvas.bind('<Button-1>', lambda x: self.to_red(True))

    def to_yellow(self, on: bool=False):
        """
        Change the LED to yellow (on or off)
        :param on: True or False
        :return: None
        """
        self._on = on
        if on:
            self._load_new(led_yellow_on)

            if self._toggle_on_click:
                self._canvas.bind('<Button-1>',
                                  lambda x: self.to_yellow(False))
        else:
            self._load_new(led_yellow)

            if self._toggle_on_click:
                self._canvas.bind('<Button-1>',
                                  lambda x: self.to_yellow(True))
