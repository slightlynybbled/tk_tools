import tkinter as tk

import pytest

from tk_tools import KeyValueEntry

from tests.test_basic import root


@pytest.fixture
def kve(root):
    kve_widget = KeyValueEntry(root, keys=['a', 'b', 'c'])
    kve_widget.grid()

    yield kve_widget


def test_creation(root):
    KeyValueEntry(root, title='blah', keys=['a', 'b', 'c'])


def test_faulty_init(root):
    with pytest.raises(ValueError):
        KeyValueEntry(root, keys=['a', 'b', 'c'], defaults=['1', '2'])

    with pytest.raises(ValueError):
        KeyValueEntry(root, keys=['a', 'b', 'c'], enables=[True, False])

    with pytest.raises(ValueError):
        KeyValueEntry(root, keys=['a', 'b', 'c'], unit_labels=['meters', 'buckets'])


def test_reset(root):
    kve = KeyValueEntry(root, keys=['a', 'b', 'c'])
    kve.grid()

    kve.load(
        {
            'a': '1', 'b': '2', 'c': '3'
        }
    )

    data = kve.get()
    assert data['a'] == '1'
    assert data['b'] == '2'
    assert data['c'] == '3'

    kve.reset()

    # todo: figure out how to verify that the entries were in fact cleared


def test_with_defaults(root):
    kve = KeyValueEntry(root, keys=['a', 'b', 'c'], defaults=['1', '2', '3'])
    kve.grid()

    kve.add_row('d')
    kve.add_row('e', default='5')


def test_enables(root):
    kve = KeyValueEntry(root, keys=['a', 'b', 'c'], enables=[True, False, False])
    kve.grid()

    kve.add_row('d')
    kve.change_enables([False, False, False, False])
