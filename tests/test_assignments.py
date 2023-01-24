import pytest

from funml import fn, let


def test_let_sets_internal_value():
    """let() a value in the internal value"""
    test_data = [
        (let(int, x=90), 90),
        (let(str, foo="bar"), "bar"),
        (let(dict, data={"bar": "bel"}), {"bar": "bel"}),
        (let(float, y=900.0), 900.0),
    ]

    for (assign, expected) in test_data:
        assert assign() == expected


def test_let_can_be_piped():
    """let() can be piped"""

    v = let(int, x=9) >> (lambda x: x + 10) >> (lambda y: y * 20) >> str

    assert v() == "380"


def test_let_sets_value_in_context():
    """let() sets a value in the context, passing it to expression as kwargs"""

    def get_context(**kwargs):
        return kwargs

    test_data = [
        (let(int, x=90), {"x": 90}),
        (let(float, y=900.0), {"y": 900.0}),
        (let(str, foo="bar"), {"foo": "bar"}),
        (let(dict, data={"bar": "bel"}), {"data": {"bar": "bel"}}),
    ]

    for (assign, expected) in test_data:
        expn = fn(assign, get_context)
        assert expn() == expected


def test_let_checks_types_when_initializing():
    """let() makes sure `value` is of right type"""
    test_data = [
        (int, "string"),
        (bytes, "foo"),
        (float, 90),
        (str, {"P": 9}),
        (dict, (9, "tuple")),
    ]

    for (t, v) in test_data:
        with pytest.raises(TypeError):
            _ = let(t, a=v)
