import tkinter as tk

import pytest

from tk_tools import SmartCheckbutton

from tests.test_basic import root


@pytest.fixture
def scb(root):
    scb_widget = SmartCheckbutton(root)
    scb_widget.grid()

    yield scb_widget


def test_creation(root):
    SmartCheckbutton(root)


def test_callback(root):
    item_value = 0

    def callback():
        nonlocal item_value
        item_value += 1

    scb = SmartCheckbutton(root, callback=callback)
    scb.grid()

    scb.set(True)
    scb.set(False)
    scb.set(True)

    assert item_value == 3


def test_callback_with_parameter(root):
    item_value = 0

    def callback(value):
        nonlocal item_value
        item_value += 2 if value else 0

    scb = SmartCheckbutton(root, callback=callback)
    scb.grid()

    scb.set(True)
    scb.set(False)
    scb.set(True)

    assert item_value == 4

