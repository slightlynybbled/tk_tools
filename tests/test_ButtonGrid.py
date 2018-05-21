import tkinter as tk

import pytest

from tk_tools import ButtonGrid

from tests.test_basic import root


@pytest.fixture
def btn_grid_3col(root):
    eg = ButtonGrid(root, 3, headers=['a', 'b', 'c'])
    yield eg

    eg._redraw()


def test_creation_with_header(root):
    ButtonGrid(root, 3, headers=['a', 'b', 'c'])


def test_header_len_doesnt_match_cols(root):
    with pytest.raises(ValueError):
        ButtonGrid(root, 2, headers=['a', 'b', 'c'])


def test_add_row(btn_grid_3col):
    data = [
        ('1', lambda: print('1')),
        ('2', lambda: print('2')),
        ('3', lambda: print('3')),
    ]
    btn_grid_3col.add_row(data)


def test_add_row_wrong_format(btn_grid_3col):
    data = ['1', '2', '3']
    with pytest.raises(ValueError):
        btn_grid_3col.add_row(data)


def test_add_row_len_doesnt_match_cols(btn_grid_3col):
    data = ['1', '2', '3', '4']

    with pytest.raises(ValueError):
        btn_grid_3col.add_row(data)


def test_remove_row(btn_grid_3col):
    data = [
        ('1', lambda: print('1')),
        ('2', lambda: print('2')),
        ('3', lambda: print('3')),
    ]
    btn_grid_3col.add_row(data)
    btn_grid_3col.add_row(data)
    btn_grid_3col.add_row(data)

    # remove row 1
    btn_grid_3col.remove_row(1)
