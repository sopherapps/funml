from functools import reduce
from typing import Any

from funml import Option, fn, match, record, l


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


def test_match_records():
    """records can be pattern matched"""
    Color = record(Color={"r": int, "g": int, "b": int, "a": int})
    User = record(User={"first": str, "last": str, "age": int})

    test_data = [
        (Color(r=0, g=0, b=255, a=0), "r:0g:0b:255a:0"),
        (Color(r=0, g=56, b=255, a=1), "Not matched"),
        (Color(r=100, g=0, b=245, a=0), "r:100g:0b:245a:0"),
        (User(first="John", last="Doe", age=67), "John 67"),
        (User(first="Jane", last="Doe", age=60), "Jane 60"),
    ]

    for arg, expected in test_data:
        value = (
            match(arg)
            .case(Color(a=0), do=fn(lambda v: f"r:{v.r}g:{v.g}b:{v.b}a:{v.a}"))
            .case(Color(), do=fn(lambda: "Not matched"))
            .case(User(last="Doe"), do=fn(lambda v: f"{v.first} {v.age}"))
            .case(User(), do=fn(lambda v: "Not matched"))
        )

        assert value() == expected


def test_match_lists():
    """lists can be pattern matched"""
    test_data = [
        (l(2, 3, 56, 34), "90"),
        (l(2, 3, 56, 36), "59"),
        (l("foo", 6.0, 89), "bar"),
        (l("foo", 6.0), "one foo"),
        (l(True, "foo", 6.0, 7), "True, foo, 6.0, 7"),
        (l(), "Empty"),
    ]

    # '...' is used to capture values to be used in the matching expression
    for arg, expected in test_data:
        value = (
            match(arg)
            .case(
                l(2, ..., 36),
                do=fn(lambda rest: f"{reduce(lambda a, b: a+b, rest, 0)}"),
            )
            .case(
                l(2, 3, ...), do=fn(lambda rest: f"{reduce(lambda a, b: a+b, rest, 0)}")
            )
            .case(l("foo", 6.0), do=fn(lambda: "one foo"))
            .case(l("foo", 6.0, ...), do=fn(lambda: "bar"))
            .case(l(...), do=fn(lambda rest: ", ".join(rest.map(lambda x: f"{x}"))))
            .case(l(), do=fn(lambda: "Empty"))
        )

        assert value() == expected
