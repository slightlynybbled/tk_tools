import tkinter as tk

import pytest

from tk_tools import MultiSlotFrame

from tests.test_basic import root


@pytest.fixture
def msf(root):
    msf_widget = MultiSlotFrame(root)
    msf_widget.grid()

    msf_widget.add('test 1')
    msf_widget.add('test 2')
    msf_widget.add('test 3')

    yield msf_widget


def test_creation(root):
    MultiSlotFrame(root)


def test_clear(msf):
    msf.clear()


def test_retrieve_values(msf):
    t1, t2, t3 = msf.get()

    assert t1 == 'test 1'
    assert t2 == 'test 2'
    assert t3 == 'test 3'
