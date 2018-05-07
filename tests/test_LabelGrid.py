import tkinter as tk

import pytest

from tk_tools import LabelGrid

from tests.test_basic import root


@pytest.fixture
def label_grid_3col(root):
    lg = LabelGrid(root, 3, headers=['a', 'b', 'c'])
    yield lg

    lg._redraw()


def test_creation_with_header(root):
    LabelGrid(root, 3, headers=['a', 'b', 'c'])


def test_header_len_doesnt_match_cols(root):
    with pytest.raises(ValueError):
        LabelGrid(root, 2, headers=['a', 'b', 'c'])


def test_add_row(label_grid_3col):
    data = ['1', '2', '3']
    label_grid_3col.add_row(data)


def test_add_row_len_doesnt_match_cols(label_grid_3col):
    data = ['1', '2', '3', '4']

    with pytest.raises(ValueError):
        label_grid_3col.add_row(data)


def test_remove_row(label_grid_3col):
    label_grid_3col.add_row(['1', '2', '3'])
    label_grid_3col.add_row(['4', '5', '6'])
    label_grid_3col.add_row(['7', '8', '9'])

    label_grid_3col.remove_row(1)

