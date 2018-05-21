import tkinter as tk

import pytest

from tk_tools import SmartOptionMenu

from tests.test_basic import root


@pytest.fixture
def som(root):
    som_widget = SmartOptionMenu(root, ['1', '2', '3'])
    som_widget.grid()

    yield som_widget


def test_creation(root):
    SmartOptionMenu(root, ['1', '2', '3'])


def test_creation_with_initial_value(root):
    som = SmartOptionMenu(root, ['1', '2', '3'], initial_value='2')

    assert som.get() == '2'


def test_callback_no_param(root):
    item_value = 0

    def callback():
        nonlocal item_value
        item_value += 1

    som = SmartOptionMenu(root, ['1', '2', '3'], callback=callback)
    som.grid()

    som.set('1')
    som.set('3')
    som.set('2')

    assert item_value == 3


def test_callback_with_param(root):
    item_value = 0

    def callback(value):
        nonlocal item_value
        item_value += int(value)

    som = SmartOptionMenu(root, ['1', '2', '3'], callback=callback)
    som.grid()

    som.set('2')
    som.set('2')
    som.set('2')

    assert item_value == 6


def test_add_callback_no_param(som):
    item_value = 0

    def callback():
        nonlocal item_value
        item_value += 1

    som.add_callback(callback)

    som.set('1')
    som.set('3')
    som.set('2')

    assert item_value == 3


def test_add_callback_with_param(som):
    item_value = 0

    def callback(value):
        nonlocal item_value
        item_value += int(value)

    som.add_callback(callback)

    som.set('2')
    som.set('2')
    som.set('2')

    assert item_value == 6
