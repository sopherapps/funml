from typing import Any

from funml import Option, fn, match


def test_match_enums():
    """enums can be pattern matched"""
    test_data = [
        (Option.SOME(90), 96),
        (Option.SOME(900), 906),
        (Option.SOME(900.0), 990.0),
        (Option.SOME("900.0"), "Unaccounted for"),
        (Option.NONE, "Come on man!"),
    ]

    for arg, expected in test_data:
        value = (
            match(arg)
            .case(Option.SOME(int), do=fn(lambda v: v + 6))
            .case(Option.SOME(float), do=fn(lambda v: v + 90))
            .case(Option.NONE, do=fn(lambda: "Come on man!"))
            .case(Option.SOME(Any), do=fn(lambda v: "Unaccounted for"))
        )

        assert value() == expected
