import tkinter as tk

import pytest

from tk_tools import EntryGrid

from tests.test_basic import root


@pytest.fixture
def entry_grid_3col(root):
    eg = EntryGrid(root, 3, headers=['a', 'b', 'c'])
    yield eg

    eg._redraw()


@pytest.fixture
def entry_grid_with_data(entry_grid_3col):
    eg = entry_grid_3col

    entry_grid_3col.add_row(['1', '2', '3'])
    entry_grid_3col.add_row(['4', '5', '6'])
    entry_grid_3col.add_row(['7', '8', '9'])

    yield eg

    eg._redraw()


def test_creation_with_header(root):
    EntryGrid(root, 3, headers=['a', 'b', 'c'])


def test_header_len_doesnt_match_cols(root):
    with pytest.raises(ValueError):
        EntryGrid(root, 2, headers=['a', 'b', 'c'])


def test_add_row(entry_grid_3col):
    data = ['1', '2', '3']
    entry_grid_3col.add_row(data)


def test_add_row_len_doesnt_match_cols(entry_grid_3col):
    data = ['1', '2', '3', '4']

    with pytest.raises(ValueError):
        entry_grid_3col.add_row(data)


def test_read_as_lists(entry_grid_with_data):
    data = entry_grid_with_data.read()

    assert data[0]['a'] == '1'
    assert data[0]['b'] == '2'
    assert data[0]['c'] == '3'
    assert data[1]['a'] == '4'
    assert data[1]['b'] == '5'
    assert data[1]['c'] == '6'
    assert data[2]['a'] == '7'
    assert data[2]['b'] == '8'
    assert data[2]['c'] == '9'


def test_remove_row(entry_grid_with_data):
    eg = entry_grid_with_data

    # remove row 1
    eg.remove_row(1)
    data = entry_grid_with_data.read()

    # now, instead of containing 4, 5, 6, row 1 should contain 7, 8, 9
    assert data[0]['a'] == '1'
    assert data[0]['b'] == '2'
    assert data[0]['c'] == '3'
    assert data[1]['a'] == '7'
    assert data[1]['b'] == '8'
    assert data[1]['c'] == '9'
