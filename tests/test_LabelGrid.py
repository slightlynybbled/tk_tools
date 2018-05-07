import tkinter as tk

import pytest

from tk_tools import LabelGrid

from tests.test_basic import root


def test_with_header(root):
    lg = LabelGrid(root, 3, headers=['a', 'b', 'c'])

    assert True


def test_header_len_doesnt_match_cols(root):
    with pytest.raises(ValueError):
        LabelGrid(root, 2, headers=['a', 'b', 'c'])

