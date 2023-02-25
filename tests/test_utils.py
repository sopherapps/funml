from __future__ import annotations

import typing
from typing import List, Any

import funml.utils as fn_utils
from tests import inspect_stock_annotations, inspect_stringized_annotations


def test_generate_random_string():
    """Generates unique random strings"""
    names = [fn_utils.generate_random_string() for _ in range(8)]
    assert len(set(names)) == 8


def test_right_pad_list():
    """right_pad_list pads a given list with the given fill_value"""
    test_data = [
        ([5, 6], "foo", 4, [5, 6, "foo", "foo"]),
        (
            (
                5,
                6,
            ),
            "foo",
            4,
            [5, 6, "foo", "foo"],
        ),
        ([5, 6], "foo", 1, [5, 6]),
        (
            (
                5,
                6,
            ),
            "foo",
            1,
            [5, 6],
        ),
    ]

    for items, fill_value, target_length, expected in test_data:
        padded_list = fn_utils.right_pad_list(
            items, fill_value=fill_value, target_length=target_length
        )
        assert padded_list == expected
