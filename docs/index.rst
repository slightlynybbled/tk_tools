.. tk_tools documentation master file, created by
   sphinx-quickstart on Thu Jan 25 06:53:00 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to tk_tools's documentation!
====================================

.. toctree::
    :maxdepth: 2

    Installation <installation.rst>
    Widget Groups <widget_groups.rst>
    Canvas Widgets <canvas_widgets.rst>
    Smart Widgets <smart_widgets.rst>

Introduction
------------

The ``tk_tools`` package exists in a space like other packages.  In many cases, the ``tkinter`` interface leaves some API to be desired while, in other cases, it leaves out some room for fairly standard visualizations.  This is a collection of widgets and tools that have been developed over the course of creating GUI elements as a means to simplify and enhance the process and results.

There are three categories of widgets:

 - groups of widgets that are useful as a group
 - visual aids using the canvas
 - useful improvements on existing widgets

Tkinter Setup
-------------

Each of the code examples assumes a structure similar to the below in order to setup the root environment.::

    import tkinter as tk
    import tk_tools

    root = tk.Tk()

    # -----------------------------------
    # ----- your GUI widget(s) here -----
    # -----------------------------------

    root.mainloop()

Indices and tables
==================

* :ref:`genindex`
