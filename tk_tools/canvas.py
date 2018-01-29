import tkinter as tk
import cmath
import sys
import logging
from decimal import Decimal

from tk_tools.images import rotary_scale, \
    led_green, led_green_on, led_yellow, led_yellow_on, \
    led_red, led_red_on, led_grey

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if getattr(sys, 'frozen', False):
    frozen = True
else:
    frozen = False

logger.info('frozen: {}'.format(frozen))


class Dial(tk.Frame):
    """
    Base class for all dials and dial-like widgets
    """
    def __init__(self, parent, size=100, **options):
        tk.Frame.__init__(self, parent, padx=3, pady=3, borderwidth=2,
                          **options)

        self.size = size

    def to_absolute(self, x, y):
        """
        Converts coordinates provided with reference to the center of the
        canvas (0, 0) to absolute coordinates which are used by the canvas
        object in which (0, 0) is located in the top left of the object.

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
    Shows a rotary scale, much like a speedometer.
    """
    def __init__(self, parent, max_value=100.0, size=100, unit='', img_data='',
                 needle_color='blue', needle_thickness=0, **options):
        """
        Initializes the RotaryScale object

        :param parent: tkinter parent frame
        :param max_value: the value corresponding to the maximum
        value on the scale
        :param size: the size in pixels
        :param options: the frame options
        """
        super().__init__(parent, size=size, **options)

        self.max_value = float(max_value)
        self.size = size
        self.unit = unit
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

    def set_value(self, number: float):
        """
        Sets the value of the graphic

        :param number: the number (must be between 0 and 'max_range'
        or the scale will peg the limits
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

    def draw_background(self, divisions=10):
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


class Graph(tk.Frame):
    """
    Tkinter native graph (pretty basic, but doesn't require heavy install)

    Notes: the core of this object was creating using the
    basic structure found at: https://gist.github.com/ajbennieston/3072649
    """
    def __init__(self, parent, x_min, x_max, y_min, y_max, x_tick, y_tick,
                 **options):
        """
        Initializes the graph object.

        :param parent: the parent frame
        :param x_min: the x minimum
        :param x_max: the x maximum
        :param y_min: the y minimum
        :param y_max: the y maximum
        :param x_tick: the 'tick' on the x-axis
        :param y_tick: the 'tick' on the y-axis
        :param options: additional valid tkinter.canvas options
        """
        tk.Frame.__init__(self, parent, **options)

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
        Removes all existing series and re-draws the axes

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
        :param point_visibility: True if the points
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
        :param step: the increment
        :param digits_to_round: the digits to which to
        round (makes floating-point numbers much easier
        to work with)
        :return: generator
        """
        while start < stop:
            yield round(start, digits_to_round)
            start += step


class Led(tk.Frame):
    """
    Create an LED-like interface for the user
    """
    def __init__(self, parent, size=100, **options):
        """
        Initialize the LED class

        :param parent: the parent frame
        :param size: the size in pixels
        :param options: the frame options
        """
        tk.Frame.__init__(self, parent, padx=3, pady=3, borderwidth=2,
                          **options)

        self.size = size

        self.canvas = tk.Canvas(self, width=self.size, height=self.size)
        self.canvas.grid(row=0)
        self.image = None

        self.to_grey()

    def _load_new(self, img_data):
        """
        Load a new image

        :param img_data: the image data as a base64 string
        :return: None
        """
        self.image = tk.PhotoImage(data=img_data)
        self.image = self.image.subsample(int(200 / self.size),
                                          int(200 / self.size))
        self.canvas.create_image(0, 0, image=self.image, anchor='nw')

    def to_grey(self):
        """
        Change the LED to grey
        :return: None
        """
        self._load_new(led_grey)

    def to_green(self, on=False):
        """
        Change the LED to green (on or off)
        :param on: True or False
        :return: None
        """
        if on:
            self._load_new(led_green_on)
        else:
            self._load_new(led_green)

    def to_red(self, on=False):
        """
        Change the LED to red (on or off)
        :param on: True or False
        :return: None
        """
        if on:
            self._load_new(led_red_on)
        else:
            self._load_new(led_red)

    def to_yellow(self, on=False):
        """
        Change the LED to yellow (on or off)
        :param on: True or False
        :return: None
        """
        if on:
            self._load_new(led_yellow_on)
        else:
            self._load_new(led_yellow)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    logging.info('frozen: {}'.format(frozen))
