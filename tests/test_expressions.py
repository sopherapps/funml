from funml import val


def test_val_literals():
    """val just creates an unnamed variable or a literal"""
    test_data = ["foo", True, 90, 909.0]

    for v in test_data:
        assert val(v)() == v


def test_val_expressions():
    """val converts a function into an expression"""
    fn = val(min) >> str
    test_data = [
        ([2, 6, 8], "2"),
        ([2, -12, 8], "-12"),
        ([20, 6, 18], "6"),
        ([0.2, 6.0, 0.08], "0.08"),
    ]

    for v, expected in test_data:
        assert fn(v) == expected


def test_val_piping():
    """val literals can be piped to other expressions"""

    v = val(900) >> (lambda x: x + 10) >> (lambda y: y * 20) >> str

    assert v() == "18200"
