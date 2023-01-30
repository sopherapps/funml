from copy import copy
from datetime import date

import pytest

from funml import val, execute, ireduce, imap, l, ifilter


def test_execute():
    """execute terminates pipeline"""
    test_data = [
        (val(90) >> (lambda x: x**2) >> (lambda v: v / 90), 90),
        (
            val("hey") >> (lambda x: f"{x} you") >> (lambda g: f"{g}, John"),
            "hey you, John",
        ),
    ]

    for pipeline, expected in test_data:
        assert (pipeline >> execute()) == expected


def test_execute_rshift_error():
    """Adding `>>` after an execute call raises NotImplementedError"""
    with pytest.raises(TypeError):
        val(90) >> (lambda x: x**2) >> execute() >> (lambda v: v / 90)

    with pytest.raises(ValueError):
        val("hey") >> execute() >> (lambda x: f"{x} you") >> (lambda g: f"{g}, John")

    with pytest.raises(NotImplementedError):
        execute() >> val("hey") >> (lambda x: f"{x} you") >> (lambda g: f"{g}, John")


def test_pipelines_can_be_combined():
    """pipelines can be combined as though they were expressions"""
    get_month = val(lambda value: value.month)
    add = val(lambda x, y: x + y)
    sum_of_months_pipeline = imap(get_month) >> ireduce(add)
    test_data = [
        (
            val(
                [
                    date(200, 3, 4),
                    date(2009, 1, 16),
                    date(1993, 12, 29),
                ]
            ),
            16,
        ),
        (
            val(
                [
                    date(2004, 10, 13),
                    date(2020, 9, 5),
                    date(2004, 5, 7),
                    date(1228, 8, 18),
                ]
            ),
            32,
        ),
    ]

    for data, expected in test_data:
        new_pipeline = data >> sum_of_months_pipeline
        got = new_pipeline >> execute()
        assert got == expected


def test_pipeline_copy():
    """copy copies the pipeline's state and returns a new pipeline."""
    is_even = val(lambda v: v % 2 == 0)
    minus_one = val(lambda v: v - 1)
    square = val(lambda v: v**2)

    test_data = [
        (l(7, 8, 6, 3), l(7, 5), "sq 8: 64\nsq 6: 36"),
        (l(4, 2, 6, 3), l(3, 1, 5), "sq 4: 16\nsq 2: 4\nsq 6: 36"),
    ]

    for nums, first_expected, second_expected in test_data:
        even_nums_pipeline = val(nums) >> ifilter(is_even)
        nums_less_1_list = copy(even_nums_pipeline) >> imap(minus_one) >> execute()
        assert list(nums_less_1_list) == list(first_expected)

        squares_str = (
            even_nums_pipeline
            >> imap(lambda v: f"sq {v}: {square(v)}")
            >> ireduce(lambda x, y: f"{x}\n{y}")
            >> execute()
        )
        assert squares_str == second_expected