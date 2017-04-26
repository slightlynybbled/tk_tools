# Purpose

This repository is intended to hold some of the most useful, higher-level widgets
that are native to tkinter.  This library is currently compatible with Python 3.5+ (uses
type hints), but could easily be back-ported to earlier versions if desired.

# Installation

For the moment, download this library and navigate to the root directory of the install.

```python 
python setup.py install
```

# Using the Widgets

All widgets are implemented as subclasses of frames and are - as a result - easily used
just as any other widget in tkinter would be utilized.  These must be placed in a frame
or toplevel using `grid()` or `pack()` just like any other frame.

# Examples

Examples of these widgets may be found within the [examples](./examples/) directory.

# Widgets



## Label Grid

The `LabelGrid` is intended to display tabular data easily and effectively.

![Label Grid](./examples/img/label-grid.png)

```python 
root = tk.Tk()

label_grid = tk_tools.LabelGrid(root, 3, ['Column0', 'Column1', 'Column2'])
label_grid.grid(row=0, column=0)

for _ in range(5):
    label_grid.add_row([1, 2, 3])

root.mainloop()
```

## Entry Grid

The `EntryGrid` is a spreadsheet-like grid of entry widgets intended to allow easy entry
of data.  When the cursor is in the bottom right entry, pressing `<Tab>` on your keyboard
will add a new row.

![Entry Grid](./examples/img/entry-grid.png)


```python 
root = tk.Tk()

entry_grid = tk_tools.EntryGrid(root, 3, ['L0', 'L1', 'L2'])
entry_grid.grid(row=0, column=0)

for _ in range(5):
    entry_grid.add_row()

root.mainloop()
```

## Key/Value

So often, it is necessary to simply extract a key/value from the user.  This widget allows
a quick creation of multiple key/value entries and supplies a `get()` method for easily
retrieving those values as a dictionary.  This can also be used as a display widget and may
have or not have titles.

Here, we are shown three key/value entries in various conditions.

![Key/Value](./examples/img/key-value.png)

```python 
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

root.mainloop()
```

## Graph

Usually, plotting is done using `matplotlib`.  Unfortunately, this is a pretty serious
installation commitment for some.  Here is an alternative simple graphing widget that
may be utilized for some plotting situations.

![Graph](./examples/img/graph.png)

Note that we can plot individual points, plot lines, and plot lines with points.

```python 
# create the graph
graph = tk_tools.Graph(
    parent=root,
    x_min=-1.0,
    x_max=1.0,
    y_min=0.0,
    y_max=2.0,
    x_scale=0.5,
    y_scale=0.5,
    width=500,
    height=400
)

graph.grid(row=0, column=0)

# create an initial line
line_0 = [(x/10, x/10) for x in range(10)]
graph.plot_line(line_0)

# plot the line with points
line_1 = [(x/5 - 1.0, x/10.0) for x in range(10)]
graph.plot_line(line_1, point_visibility=True)

# plot a single point
point = (0.5, 0.75)
graph.plot_point(*point)
```

## Rotary Scale

The `RotaryScale` looks much like a speedometer.  It is used when a quick graphical
indicator is needed.  It could probably use some look-and-feel improvements, but
will do the job.

![Rotary Scale](./examples/img/rotary-scale.png)

```python 
p = tk_tools.RotaryScale(root, max_value=20.0)
p.grid(row=0, column=0)

p.set_value(5)
```


