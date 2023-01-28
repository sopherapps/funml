import pytest

from funml import Result, let, if_ok, Option, record, if_err, if_some, if_none, val
from funml.errors import MatchError


@record
class Color:
    r: int
    g: int
    b: int


def test_if_ok():
    """if_ok only runs do when value is Result.OK, else returns the Result.ERR"""
    test_data = [
        # do/return, value, expected
        ("excellent", Result.OK(90), "excellent"),
        (val("excellent"), Result.OK(90), "excellent"),
        (lambda v: v * 20, Result.OK(9), 180),
        (val(lambda v: v * 20), Result.OK(9), 180),
        (let(int, h=60), Result.OK("yeah"), {"h": 60}),
        ("excellent", Result.ERR(ValueError()), Result.ERR(ValueError())),
        (val("excellent"), Result.ERR(ValueError()), Result.ERR(ValueError())),
        (lambda v: v * 20, Result.ERR(Exception()), Result.ERR(Exception())),
        (let(int, h=60), Result.ERR(TypeError()), Result.ERR(TypeError())),
    ]

    for do, value, expected in test_data:
        assert if_ok(do)(value) == expected


def test_if_err():
    """if_err only runs do when value is Result.ERR, else returns the Result.OK"""
    test_data = [
        # do/return, value, expected
        ("excellent", Result.ERR(ValueError()), "excellent"),
        (val("excellent"), Result.ERR(ValueError()), "excellent"),
        (lambda v: str(v), Result.ERR(Exception("error")), "error"),
        (val(lambda v: str(v)), Result.ERR(Exception("error")), "error"),
        (let(int, h=60), Result.ERR(TypeError()), {"h": 60}),
        ("excellent", Result.OK(90), Result.OK(90)),
        (lambda v: v * 20, Result.OK(9), Result.OK(9)),
        (val(lambda v: v * 20), Result.OK(9), Result.OK(9)),
        (let(int, h=60), Result.OK("yeah"), Result.OK("yeah")),
    ]

    for do, value, expected in test_data:
        assert if_err(do)(value) == expected


def test_if_ok_if_err_match_error():
    """if_ok and if_err raise MatchError if value passed is not a Result and strict is True"""
    test_data = [
        # do/return, value
        ("excellent", 90),
        (lambda v: v * 20, "Result.OK(9)"),
        (val(lambda v: v * 20), "Result.OK(9)"),
        (let(int, h=60), Option.SOME("yeah")),
        ("excellent", None),
        (lambda v: v * 20, dict(h=90)),
        (val(lambda v: v * 20), dict(h=90)),
        (let(int, h=60), Color(r=6, b=90, g=78)),
    ]

    for do, value in test_data:
        with pytest.raises(MatchError):
            _ = if_ok(do)(value)

        with pytest.raises(MatchError):
            _ = if_err(do)(value)

        assert if_ok(do, strict=False)(value) == value
        assert if_err(do, strict=False)(value) == value


def test_if_some():
    """if_some only runs do when value is Option.SOME, else returns the Option.NONE"""
    test_data = [
        # do/return, value, expected
        ("excellent", Option.SOME(90), "excellent"),
        (lambda v: v * 20, Option.SOME(9), 180),
        (val(lambda v: v * 20), Option.SOME(9), 180),
        (let(int, h=60), Option.SOME("yeah"), {"h": 60}),
        ("excellent", Option.NONE, Option.NONE),
        (lambda v: v * 20, Option.NONE, Option.NONE),
        (val(lambda v: v * 20), Option.NONE, Option.NONE),
        (let(int, h=60), Option.NONE, Option.NONE),
    ]

    for do, value, expected in test_data:
        assert if_some(do)(value) == expected


def test_if_none():
    """if_none only runs do when value is Option.NONE, else returns the Option.SOME"""
    test_data = [
        # do/return, value, expected
        ("excellent", Option.NONE, "excellent"),
        (lambda v: 180, Option.NONE, 180),
        (val(lambda v: 180), Option.NONE, 180),
        (let(int, h=60), Option.NONE, {"h": 60}),
        ("excellent", Option.SOME(90), Option.SOME(90)),
        (lambda v: v * 20, Option.SOME(9), Option.SOME(9)),
        (val(lambda v: v * 20), Option.SOME(9), Option.SOME(9)),
        (let(int, h=60), Option.SOME("yeah"), Option.SOME("yeah")),
    ]

    for do, value, expected in test_data:
        assert if_none(do)(value) == expected


def test_if_some_if_none_match_error():
    """if_some and if_none raise MatchError if value passed is not an Option and strict is True"""
    test_data = [
        # do/return, value
        ("excellent", 90),
        (lambda v: v * 20, "Option.SOME(9)"),
        (val(lambda v: v * 20), "Option.SOME(9)"),
        (let(int, h=60), Result.OK("yeah")),
        ("excellent", None),
        (lambda v: v * 20, dict(h=90)),
        (val(lambda v: v * 20), dict(h=90)),
        (let(int, h=60), Color(r=6, b=90, g=78)),
    ]

    for do, value in test_data:
        with pytest.raises(MatchError):
            _ = if_some(do)(value)

        with pytest.raises(MatchError):
            _ = if_none(do)(value)

        assert if_some(do, strict=False)(value) == value
        assert if_none(do, strict=False)(value) == value
