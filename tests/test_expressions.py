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


def test_expressions_are_pure():
    """expressions have no hidden side effects"""
    unit = lambda v: v
    tester = lambda v, *args: v <= 0
    if_else = lambda check=unit, do=unit, else_do=unit: lambda *args, **kwargs: (
        do(*args, **kwargs) if check(*args, **kwargs) else else_do(*args, **kwargs)
    )

    accum_factrl = if_else(
        check=tester,
        do=lambda v, accum: accum,
        else_do=lambda v, accum: accum_factrl(v - 1, v * accum),
    )
    pure_factorial = lambda v: accum_factrl(v, 1)

    unit_expn = val(lambda v: v)
    if_else_expn = val(
        lambda check=unit_expn, do=unit_expn, else_do=unit_expn: lambda *args, **kwargs: (
            do(*args, **kwargs) if check(*args, **kwargs) else else_do(*args, **kwargs)
        )
    )

    accum_factrl_expn = if_else_expn(
        check=val(tester),
        do=val(lambda v, accum: accum),
        else_do=val(lambda v, accum: accum_factrl_expn(v - 1, v * accum)),
    )
    factorial_expn = val(lambda v: accum_factrl_expn(v, 1))

    test_data = [
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
        (6, 720),
        (7, 5040),
        (8, 40320),
        (9, 362880),
        (10, 3628800),
    ]

    for value, expected in test_data:
        assert pure_factorial(value) == expected
        assert factorial_expn(value) == expected
