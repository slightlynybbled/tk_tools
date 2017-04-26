import tkinter as tk
import cmath


class Dial(tk.Frame):
    """
    Base class for all dials and dial-like widgets
    """
    def __init__(self, parent, size=100, **options):
        tk.Frame.__init__(self, parent, padx=3, pady=3, borderwidth=2, **options)

        self.size = size

    def to_absolute(self, x, y):
        """
        Converts coordinates provided with reference to the center of the canvas (0, 0)
        to absolute coordinates which are used by the canvas object in which (0, 0) is
        located in the top left of the object.
        
        :param x: x value in pixels
        :param y: x value in pixels
        :return: 
        """
        return x + self.size/2, y + self.size/2


class Compass(Dial):
    """
    Displays a compass typically seen on a map
    """
    def __init__(self, parent, size=100, **options):
        super().__init__(parent, size=size, **options)
        raise NotImplementedError()

        # todo: import an image, place the image on the canvas, then place an arrow on top of the image


class RotaryScale(Dial):
    """
    Shows a rotary scale, much like a speedometer.
    """
    def __init__(self, parent, max_value=100.0, size=100, **options):
        """
        Initializes the RotaryScale object
        
        :param parent: tkinter parent frame
        :param max_value: the value corresponding to the maximum value on the scale
        :param size: the size in pixels
        :param options: the frame options
        """
        super().__init__(parent, size=size, **options)

        self.max_value = float(max_value)
        self.size = size

        self.canvas = tk.Canvas(self, width=self.size, height=self.size)
        self.canvas.grid()

        initial_value = 0.0
        self.set_value(initial_value)

    def set_value(self, number: float):
        """
        Sets the value of the graphic
        
        :param number: the number (must be between 0 and 'max_range' or the scale will peg the limits
        :return: None
        """
        self.canvas.delete('all')
        self.draw_background()

        number = number if number <= self.max_value else self.max_value
        number = 0.0 if number < 0.0 else number

        radius = 0.9 * self.size/2.0
        angle_in_radians = (2.0 * cmath.pi / 3.0) + number / self.max_value * (5.0 * cmath.pi / 3.0)

        center = cmath.rect(0, 0)
        outer = cmath.rect(radius, angle_in_radians)

        self.canvas.create_line(
            *self.to_absolute(center.real, center.imag),
            *self.to_absolute(outer.real, outer.imag),
            width=5
        )

    def draw_background(self, divisions=10):
        """
        Draws the background of the dial
        
        :param divisions: the number of divisions between 'ticks' shown on the dial
        :return: 
        """
        self.canvas.create_arc(2, 2, self.size-2, self.size-2, style=tk.PIESLICE, start=-60, extent=30, fill='red')
        self.canvas.create_arc(2, 2, self.size-2, self.size-2, style=tk.PIESLICE, start=-30, extent=60, fill='yellow')
        self.canvas.create_arc(2, 2, self.size-2, self.size-2, style=tk.PIESLICE, start=30, extent=210, fill='green')

        # find the distance between the center and the inner tick radius
        inner_tick_radius = int(self.size * 0.4)
        outer_tick_radius = int(self.size * 0.5)

        for tick in range(divisions):
            angle_in_radians = (2.0 * cmath.pi / 3.0) + tick/divisions * (5.0 * cmath.pi / 3.0)
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
    def __init__(self, parent, x_min, x_max, y_min, y_max, x_scale, y_scale, **options):
        """
        Initializes the graph object.
        
        :param parent: the parent frame
        :param x_min: the x minimum
        :param x_max: the x maximum
        :param y_min: the y minimum
        :param y_max: the y maximum
        :param x_scale: the 'tick' on the x-axis
        :param y_scale: the 'tick' on the y-axis
        :param options: additional valid tkinter.canvas options
        """
        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self, **options)
        self.canvas.grid(row=0, column=0)

        self.w = float(self.canvas.config('width')[4])
        self.h = float(self.canvas.config('height')[4])
        self.x_min = x_min
        self.x_max = x_max
        self.x_scale = x_scale
        self.y_min = y_min
        self.y_max = y_max
        self.y_scale = y_scale
        self.px_x = (self.w - 100) / ((x_max - x_min) / x_scale)
        self.px_y = (self.h - 100) / ((y_max - y_min) / y_scale)

        self.draw_axes()

    def draw_axes(self):
        """
        Removes all existing series and re-draws the axes
        
        :return: None 
        """
        self.canvas.delete('all')
        rect = 50, 50, self.w - 50, self.h - 50

        self.canvas.create_rectangle(rect, outline="black")

        for x in self.frange(0, self.x_max - self.x_min + 1, self.x_scale):
            x_step = (self.px_x * x) / self.x_scale
            coord = 50 + x_step, self.h - 50, 50 + x_step, self.h - 45
            self.canvas.create_line(coord, fill="black")
            coord = 50 + x_step, self.h - 40
            self.canvas.create_text(coord, fill="black", text=str(self.x_min + x))

        for y in self.frange(0, self.y_max - self.y_min + 1, self.y_scale):
            y_step = (self.px_y * y) / self.y_scale
            coord = 45, 50 + y_step, 50, 50 + y_step
            self.canvas.create_line(coord, fill="black")
            coord = 35, 50 + y_step
            self.canvas.create_text(coord, fill="black", text=str(self.y_max - y))

    def plot_point(self, x, y, visible=True, color='black', size=5):
        """
        Places a single point on the 
        :param x: 
        :param y: 
        :param visible: True if the individual point should be visible
        :param color: the color of the point
        :param size: the point size in pixels
        :return: 
        """
        xp = (self.px_x * (x - self.x_min)) / self.x_scale
        yp = (self.px_y * (self.y_max - y)) / self.y_scale
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

    def plot_line(self, points, color='black', point_visibility=False):
        """
        Plot a line of points
        
        :param points: a list of tuples, each tuple containing an (x, y) point
        :param color: the color of the line
        :param point_visibility: True if the points should be individually visible
        :return: None
        """
        last_point = ()
        for point in points:
            this_point = self.plot_point(point[0], point[1], color=color, visible=point_visibility)

            if last_point:
                self.canvas.create_line(last_point + this_point, fill=color)
            last_point = this_point
            # print last_point

    @staticmethod
    def frange(x, y, jump, digits_to_round=3):
        while x < y:
            yield round(x, digits_to_round)
            x += jump


if __name__ == '__main__':
    root = tk.Tk()

    p = RotaryScale(root, max_value=20.0)
    p.grid(row=0, column=0)

    increment = 1.0
    value = 0.0

    def inc():
        global value
        value += increment
        p.set_value(value)
        print(value)

    zero_btn = tk.Button(root, text='increment by {}'.format(increment), command=inc)
    zero_btn.grid(row=1, column=0)



    root.mainloop()

