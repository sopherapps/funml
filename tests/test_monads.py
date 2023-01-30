import pytest

from funml import (
    Result,
    if_ok,
    Option,
    record,
    if_err,
    if_some,
    if_none,
    val,
    is_ok,
    is_err,
    is_some,
    is_none,
)
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
        ("excellent", Result.ERR(ValueError()), Result.ERR(ValueError())),
        (val("excellent"), Result.ERR(ValueError()), Result.ERR(ValueError())),
        (lambda v: v * 20, Result.ERR(Exception()), Result.ERR(Exception())),
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
        ("excellent", Result.OK(90), Result.OK(90)),
        (lambda v: v * 20, Result.OK(9), Result.OK(9)),
        (val(lambda v: v * 20), Result.OK(9), Result.OK(9)),
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
        ("excellent", None),
        (lambda v: v * 20, dict(h=90)),
        (val(lambda v: v * 20), dict(h=90)),
    ]

    for do, value in test_data:
        with pytest.raises(MatchError):
            _ = if_ok(do)(value)

        with pytest.raises(MatchError):
            _ = if_err(do)(value)

        assert if_ok(do, strict=False)(value) == value
        assert if_err(do, strict=False)(value) == value


def test_is_ok():
    """is_ok returns True value is Result.OK, else False"""
    test_data = [
        # value, expected
        (Result.OK(90), True),
        (Result.OK(9.90), True),
        (Result.OK("yeah"), True),
        (Result.ERR(ValueError()), False),
        (Result.ERR(Exception()), False),
        (Result.ERR(TypeError()), False),
    ]

    for value, expected in test_data:
        assert is_ok(value) == expected


def test_is_err():
    """is_err returns True value is Result.ERR, else False"""
    test_data = [
        # value, expected
        (Result.OK(90), False),
        (Result.OK(9.90), False),
        (Result.OK("yeah"), False),
        (Result.ERR(ValueError()), True),
        (Result.ERR(Exception()), True),
        (Result.ERR(TypeError("woo-hoo")), True),
    ]

    for value, expected in test_data:
        assert is_err(value) == expected


def test_is_ok_is_err_match_error():
    """is_ok and is_err raise MatchError if value passed is not a Result and strict is True"""
    test_data = [
        90,
        "Result.OK(9)",
        90.0,
        Option.SOME("yeah"),
        None,
        dict(h=90),
    ]

    for value in test_data:
        with pytest.raises(MatchError):
            _ = is_ok(value)

        with pytest.raises(MatchError):
            _ = is_err(value)

        assert not is_ok(value, strict=False)
        assert not is_err(value, strict=False)


def test_if_some():
    """if_some only runs do when value is Option.SOME, else returns the Option.NONE"""
    test_data = [
        # do/return, value, expected
        ("excellent", Option.SOME(90), "excellent"),
        (lambda v: v * 20, Option.SOME(9), 180),
        (val(lambda v: v * 20), Option.SOME(9), 180),
        ("excellent", Option.NONE, Option.NONE),
        (lambda v: v * 20, Option.NONE, Option.NONE),
        (val(lambda v: v * 20), Option.NONE, Option.NONE),
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
        ("excellent", Option.SOME(90), Option.SOME(90)),
        (lambda v: v * 20, Option.SOME(9), Option.SOME(9)),
        (val(lambda v: v * 20), Option.SOME(9), Option.SOME(9)),
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
        ("excellent", None),
        (lambda v: v * 20, dict(h=90)),
        (val(lambda v: v * 20), dict(h=90)),
    ]

    for do, value in test_data:
        with pytest.raises(MatchError):
            _ = if_some(do)(value)

        with pytest.raises(MatchError):
            _ = if_none(do)(value)

        assert if_some(do, strict=False)(value) == value
        assert if_none(do, strict=False)(value) == value


def test_is_some():
    """is_some returns True value is Option.SOME, else False"""
    test_data = [
        # value, expected
        (Option.SOME(90), True),
        (Option.SOME(9.90), True),
        (Option.SOME("yeah"), True),
        (Option.NONE, False),
        (Option.NONE, False),
        (Option.NONE, False),
    ]

    for value, expected in test_data:
        assert is_some(value) == expected


def test_is_none():
    """is_none returns True value is Option.NONE, else False"""
    test_data = [
        # value, expected
        (Option.SOME(90), False),
        (Option.SOME(9.90), False),
        (Option.SOME("yeah"), False),
        (Option.NONE, True),
        (Option.NONE, True),
        (Option.NONE, True),
    ]

    for value, expected in test_data:
        assert is_none(value) == expected


def test_is_some_is_none_match_error():
    """is_some and is_none raise MatchError if value passed is not an Option and strict is True"""
    test_data = [
        90,
        "Option.OK(9)",
        90.0,
        Result.OK("yeah"),
        None,
        dict(h=90),
    ]

    for value in test_data:
        with pytest.raises(MatchError):
            _ = is_some(value)

        with pytest.raises(MatchError):
            _ = is_none(value)

        assert not is_some(value, strict=False)
        assert not is_none(value, strict=False)
