import tkinter as tk

import pytest

from tk_tools import *


@pytest.fixture
def create_root():
    root = tk.Tk()
    yield root


def test_init(create_root):
    """
    Ensures that all elements of the GUI may be instantiated
    without errors.
    """
    RotaryScale(create_root)
    Gauge(create_root)
    Graph(create_root, 0, 10, 0, 10, 0.1, 0.1)
    Led(create_root)
    EntryGrid(create_root, 3)
    LabelGrid(create_root, 3)
    ButtonGrid(create_root, 3)
    KeyValueEntry(create_root, keys=['1', '2'])
    SmartOptionMenu(create_root, ['1', '2'])
    SmartSpinBox(create_root)
    SmartCheckbutton(create_root)
    Calendar(create_root)
    MultiSlotFrame(create_root)
    SevenSegmentDigits(create_root)
    BinaryLabel(create_root)
    ToolTip(BinaryLabel(create_root), 'some text')

    assert True
