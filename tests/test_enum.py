from funml import Option, Result


def test_builtin_enums():
    """enums: Option and Result act as expected"""
    a = Option.NONE
    b = Option.SOME(6)
    b2 = Option.SOME(60)
    b3 = Option.SOME(60)
    c = Result.OK(900)
    d = Result.ERR(TypeError)

    assert b2 != b
    assert b3 == b2
    assert a != b
    assert c != d
    assert not (b2 <= b)
    assert b3 <= b2
    assert not (a <= b)
    assert not (c <= d)
