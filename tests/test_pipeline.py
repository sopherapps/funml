import pytest

from funml import val, execute


def test_execute():
    """execute terminates pipeline"""
    test_data = [
        (val(90) >> (lambda x: x**2) >> (lambda v: v / 90), 90),
        (
            val("hey") >> (lambda x: f"{x} you") >> (lambda g: f"{g}, John"),
            "hey you, John",
        ),
    ]

    for pipe, expected in test_data:
        assert (pipe >> execute()) == expected


def test_execute_rshift_error():
    """Adding `>>` after an execute call raises NotImplementedError"""
    with pytest.raises(TypeError):
        val(90) >> (lambda x: x**2) >> execute() >> (lambda v: v / 90)

    with pytest.raises(TypeError):
        val("hey") >> execute() >> (lambda x: f"{x} you") >> (lambda g: f"{g}, John")

    with pytest.raises(NotImplementedError):
        execute() >> val("hey") >> (lambda x: f"{x} you") >> (lambda g: f"{g}, John")
