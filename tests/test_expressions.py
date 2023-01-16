from funml.assignments import let
from funml.expressions import fn


def test_expression_composition():
    """Expressions can be composed from multiple expressions"""
    add = lambda x, a: x + a

    add7 = fn(
        let(int, a=7),
        add,
    )

    test_data = [(7, 14), (4, 11), (21, 28), (70, 77)]

    for (v, expected) in test_data:
        assert add7(v) == expected
