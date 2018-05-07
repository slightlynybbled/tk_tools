import tkinter as tk

import pytest

from tk_tools import *


@pytest.fixture
def root():
    root_frame = tk.Tk()
    yield root_frame


def test_version():
    assert isinstance(__version__, str)


def test_init(root):
    """
    Ensures that all elements of the GUI may be instantiated
    without errors.
    """
    RotaryScale(root).grid()
    Gauge(root).grid()
    Graph(root, 0, 10, 0, 10, 0.1, 0.1).grid()
    Led(root).grid()
    EntryGrid(root, 3).grid()
    LabelGrid(root, 3).grid()
    ButtonGrid(root, 3).grid()
    KeyValueEntry(root, keys=['1', '2']).grid()
    SmartOptionMenu(root, ['1', '2']).grid()
    SmartSpinBox(root).grid()
    SmartCheckbutton(root).grid()
    Calendar(root).grid()
    MultiSlotFrame(root).grid()
    SevenSegmentDigits(root).grid()
    BinaryLabel(root).grid()

    bl = BinaryLabel(root)
    bl.grid()
    ToolTip(bl, 'some text')

    # if the test suite makes it to here, then all widgets
    # have been successfully instantiated
    assert True




