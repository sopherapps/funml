from typing import Optional

import pytest

from funml.data.records import record


def test_records_created():
    """record creates distinct records"""

    Color = record({"r": int, "g": int, "b": int, "a": int})

    blue = Color(r=0, g=0, b=255, a=1)
    red = Color(r=255, g=0, b=0, a=1)
    green = Color(r=0, g=255, b=0, a=1)

    another_blue = Color(r=0, g=0, b=255, a=1)
    another_red = Color(r=255, g=0, b=0, a=1)
    another_green = Color(r=0, g=255, b=0, a=1)

    assert blue == another_blue
    assert green == another_green
    assert red == another_red

    assert blue != green
    assert red != blue
    assert green != red


def test_unexpected_fields():
    """Unexpected fields throw error"""
    Color = record({"r": int, "g": int, "b": int, "a": Optional[int]})

    try:
        _ = Color(r=56, g=4, b=45)  # no error
    except Exception as exc:
        assert False, f"'Color' raised an exception {exc}"

    with pytest.raises(TypeError):
        _ = Color(r=56, o=45, a=5)


def test_no_extra_fields():
    """No extra fields are allowed"""
    Color = record({"r": int, "g": int, "b": int, "a": int})

    with pytest.raises(TypeError):
        _ = Color(r=56, g=4, b=45, a=5, y=0)
