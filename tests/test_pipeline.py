from datetime import date

import pytest

from funml import val, execute, match, ireduce, l, imap


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
