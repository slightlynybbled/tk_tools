import tkinter as tk

import pytest

from tk_tools import *

from tests.test_basic import root


def test_LabelGrid_header_len_doesnt_match_cols(root):
    with pytest.raises(ValueError):
        LabelGrid(root, 2, headers=['a', 'b', 'c'])

