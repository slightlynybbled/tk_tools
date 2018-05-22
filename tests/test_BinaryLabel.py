import tkinter as tk

import pytest

from tk_tools import BinaryLabel

from tests.test_basic import root


@pytest.fixture
def bl(root):
    bl_widget = BinaryLabel(root)
    bl_widget.grid()

    yield bl_widget


def test_creation(root):
    bl = BinaryLabel(root)
    bl.grid()

    assert bl.get() == 0


def test_creation_with_value(root):
    bl = BinaryLabel(root, value=101)
    bl.grid()

    assert bl.get() == 101


def test_change_value(bl):
    bl.set(101)
    assert bl.get() == 101

    bl.set(10)
    assert bl.get() == 10


def test_change_value_too_large(bl):
    with pytest.raises(ValueError):
        bl.set(0x100)


def test_get_bit(bl):
    bl.set(0x55)

    assert bl.get_bit(0) == 1
    assert bl.get_bit(1) == 0
    assert bl.get_bit(2) == 1
    assert bl.get_bit(3) == 0
    assert bl.get_bit(4) == 1
    assert bl.get_bit(5) == 0
    assert bl.get_bit(6) == 1
    assert bl.get_bit(7) == 0

    with pytest.raises(ValueError):
        bl.get_bit(8)


def test_toggle_bit(bl):
    bl.set(0x55)
    assert bl.get_bit(0) == 1

    bl.toggle_bit(0)
    assert bl.get_bit(0) == 0

    with pytest.raises(ValueError):
        bl.toggle_bit(8)


def test_set_and_clear_bit(bl):
    bl.set(0x55)
    assert bl.get_bit(0) == 1

    bl.clear_bit(0)
    assert bl.get_bit(0) == 0

    bl.set_bit(0)
    assert bl.get_bit(0) == 1

    with pytest.raises(ValueError):
        bl.clear_bit(8)

    with pytest.raises(ValueError):
        bl.set_bit(8)


def test_get_msb_and_lsb(bl):
    assert bl.get_msb() == 0
    assert bl.get_lsb() == 0

    bl.set(0xff)
    assert bl.get_msb() == 1
    assert bl.get_lsb() == 1


def test_set_msb(bl):
    assert bl.get() == 0

    bl.set_msb()
    assert bl.get() == 0x80


def test_clear_msb(bl):
    bl.set(0xff)
    assert bl.get() == 0xff

    bl.clear_msb()
    assert bl.get() == 0x7f


def test_set_lsb(bl):
    assert bl.get() == 0

    bl.set_lsb()
    assert bl.get() == 0x01


def test_clear_lsb(bl):
    bl.set(0xff)
    assert bl.get() == 0xff

    bl.clear_lsb()
    assert bl.get() == 0xfe


def test_toggle_msb_lsb(bl):
    bl.toggle_msb()
    bl.toggle_lsb()
    assert bl.get() == 0x81

    bl.toggle_msb()
    bl.toggle_lsb()
    assert bl.get() == 0x00

