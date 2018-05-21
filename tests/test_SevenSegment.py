import tkinter as tk

import pytest

from tk_tools import SevenSegmentDigits

from tests.test_basic import root


@pytest.fixture
def ssd(root):
    ssd_widget = SevenSegmentDigits(root, digits=3)
    ssd_widget.grid()

    yield ssd_widget


def test_creation(root):
    SevenSegmentDigits(root)


def test_set_value_str(ssd):
    ssd.set_value('98.7')
