import pytest

from funml import Option, Result, data


def test_enum_creation():
    """enum and e are used to create enums"""

    class Date(data.enum.Enum):
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
