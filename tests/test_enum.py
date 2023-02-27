from typing import List, Dict, Tuple

import pytest

from funml import Option, Result, Enum, record, to_json, from_json
from tests import conftest


def test_enum_creation():
    """enum and e are used to create enums"""

    class Date(Enum):
        January = int
        February = int
        March = int
        April = int
        May = int
        June = int
        July = int
        August = int
        September = int
        October = int
        November = int
        December = int

    fifth_march = Date.March(5)
    sixth_march = Date.March(6)
    another_sixth_march = Date.March(6)
    twentieth_may = Date.May(20)
    thirtieth_december = Date.December(30)

    assert sixth_march == another_sixth_march
    assert sixth_march != fifth_march
    assert twentieth_may != thirtieth_december
    assert twentieth_may != sixth_march
    assert twentieth_may != fifth_march
    assert thirtieth_december != sixth_march
    assert thirtieth_december != fifth_march


def test_builtin_enums():
    """enums: Option and Result act as expected"""
    a = Option.NONE
    b = Option.SOME(6)
    b2 = Option.SOME(60)
    b3 = Option.SOME(60)
    c = Result.OK(900)
    d = Result.ERR(TypeError("some error"))
    # works when associated data is the EXACT type as in definition.
    # this is useful when pattern matching
    e = Result.ERR(Exception)

    assert b2 != b
    assert b3 == b2
    assert a != b
    assert c != d
    assert isinstance(e, Result.ERR)


def test_enum_type_check():
    """Associated data should be of the expected type"""
    with pytest.raises(Exception):
        _ = Option.NONE(0)

    with pytest.raises(TypeError):
        _ = Result.ERR(0)

    with pytest.raises(TypeError):
        # we need either an instance of the class or the class itself
        _ = Result.ERR(ValueError)

    with pytest.raises(TypeError):
        _ = Result.ERR(None)


def test_enum_name():
    """The name attribute returns the name of the enum"""
    assert Result.OK(0).name == "Result.OK"
    assert Result.ERR(TypeError("some error")).name == "Result.ERR"
    assert Option.NONE.name == "Option.NONE"
    assert Option.SOME(345.89).name == "Option.SOME"


def test_to_json():
    """to_json transforms enum into a JSON string representation of enum"""

    @record
    class Number:
        num: int
        decimals: List[int]

    class Alpha(Enum):
        OPAQUE = None
        TRANSLUCENT_AS_NUM = (Number,)
        TRANSLUCENT_AS_LIST = List[Number]
        TRANSLUCENT_AS_DICT = {"num": int, "decimals": List[str]}
        TRANSLUCENT_AS_DICT_ANNOTATION = Dict[str, int]
        TRANSLUCENT_AS_TUPLE_ANNOTATION = Tuple[int, ...]

    test_data = [
        (Alpha.OPAQUE, '"Alpha.OPAQUE: \\"OPAQUE\\""'),
        (
            Alpha.TRANSLUCENT_AS_NUM(Number(num=12, decimals=[8, 7])),
            '"Alpha.TRANSLUCENT_AS_NUM: [{"num": 12, "decimals": [8, 7]}]"',
        ),
        (
            Alpha.TRANSLUCENT_AS_LIST([Number(num=20, decimals=[80, 7])]),
            '"Alpha.TRANSLUCENT_AS_LIST: [{"num": 20, "decimals": [80, 7]}]"',
        ),
        (
            Alpha.TRANSLUCENT_AS_DICT(dict(num=24, decimals=[8, 6])),
            '"Alpha.TRANSLUCENT_AS_DICT: {"num": 24, "decimals": [8, 6]}"',
        ),
        (
            Alpha.TRANSLUCENT_AS_DICT_ANNOTATION(dict(num=204, decimal=8)),
            '"Alpha.TRANSLUCENT_AS_DICT_ANNOTATION: {"num": 204, "decimal": 8}"',
        ),
        (
            Alpha.TRANSLUCENT_AS_TUPLE_ANNOTATION(
                (
                    204,
                    8,
                )
            ),
            '"Alpha.TRANSLUCENT_AS_TUPLE_ANNOTATION: [204, 8]"',
        ),
    ]

    for item, expected in test_data:
        assert to_json(item) == expected


def test_from_json():
    """from_json transforms a JSON string representation into an Enum"""

    @record
    class Number:
        num: int
        decimals: List[int]

    class Alpha(Enum):
        OPAQUE = None
        TRANSLUCENT_AS_NUM = (Number,)
        TRANSLUCENT_AS_LIST = List[Number]
        TRANSLUCENT_AS_DICT = {"num": int, "decimals": List[str]}
        TRANSLUCENT_AS_DICT_ANNOTATION = Dict[str, int]
        TRANSLUCENT_AS_TUPLE_ANNOTATION = Tuple[int, ...]

    test_data = [
        ('"Alpha.OPAQUE: \\"OPAQUE\\""', Alpha.OPAQUE),
        (
            '"Alpha.TRANSLUCENT_AS_NUM: [{"num": 12, "decimals": [8, 7]}]"',
            Alpha.TRANSLUCENT_AS_NUM(Number(num=12, decimals=[8, 7])),
        ),
        (
            '"Alpha.TRANSLUCENT_AS_LIST: [{"num": 20, "decimals": [80, 7]}]"',
            Alpha.TRANSLUCENT_AS_LIST([Number(num=20, decimals=[80, 7])]),
        ),
        (
            '"Alpha.TRANSLUCENT_AS_DICT: {"num": 24, "decimals": [8, 6]}"',
            Alpha.TRANSLUCENT_AS_DICT(dict(num=24, decimals=[8, 6])),
        ),
        (
            '"Alpha.TRANSLUCENT_AS_DICT_ANNOTATION: {"num": 204, "decimal": 8}"',
            Alpha.TRANSLUCENT_AS_DICT_ANNOTATION(dict(num=204, decimal=8)),
        ),
        (
            '"Alpha.TRANSLUCENT_AS_TUPLE_ANNOTATION: [204, 8]"',
            Alpha.TRANSLUCENT_AS_TUPLE_ANNOTATION(
                (
                    204,
                    8,
                )
            ),
        ),
    ]

    for item, expected in test_data:
        assert from_json(Alpha, item) == expected


def test_from_json_strict():
    """from_json with strict transforms a JSON string representation into an Enum or errors"""
    test_data = [
        '"Alph.OPAQUE: "OPAQUE""',
        '"OPAQUE: "OPAQUE""',
        '"TRANSLUCENT: 0.9"',
    ]

    for item in test_data:
        with pytest.raises(ValueError, match=r"unable to deserialize JSON.*"):
            from_json(conftest.Alpha, item)

        assert from_json(conftest.Alpha, item, strict=False) == item
