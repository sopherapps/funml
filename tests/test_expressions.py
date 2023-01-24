from funml import fn, let, val


def test_expression_composition():
    """Expressions can be composed from multiple expressions"""
    add = lambda x, a: x + a

    add7 = fn(let(int, a=7), add)

    test_data = [(7, 14), (4, 11), (21, 28), (70, 77)]

    for (v, expected) in test_data:
        assert add7(v) == expected


def test_expression_piping():
    """Expressions can be composed from multiple expressions by piping"""

    v = val(900) >> (lambda x: x + 10) >> (lambda y: y * 20) >> str

    assert v() == "18200"


def test_single_value_fn_is_same_as_val():
    """Expressions defined as fn(v) == val(v)"""
    test_data = [
        (val(900), fn(900)),
        (val(None), fn()),
        (val(None), fn(None)),
    ]
    for (expn1, expn2) in test_data:
        assert expn1() == expn2()
