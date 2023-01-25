import dataclasses
from functools import reduce
from typing import Any

from funml import Option, match, record, l


def test_match_any_type():
    """match can match built in types or other custom types"""

    @dataclasses.dataclass
    class Dummy:
        age: int
        name: str

        def __str__(self):
            return f"{self.__dict__}"

    test_data = [
        ("hey", "str"),
        (900, 9000),
        (900.9, "float"),
        (Dummy(age=90, name="Roe"), "{'age': 90, 'name': 'Roe'}"),
        ({"dict": "yeah"}, "Any"),
    ]

    for arg, expected in test_data:
        value = (
            match(arg)
            .case(int, do=lambda v: v * 10)
            .case(str, do=lambda: "str")
            .case(float, do=lambda: "float")
            .case(Dummy, do=lambda v: f"{v}")
            .case(..., do=lambda: "Any")
        )

        assert value() == expected


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
            .case(Option.SOME(int), do=lambda v: v + 6)
            .case(Option.SOME(float), do=lambda v: v + 90)
            .case(Option.NONE, do=lambda: "Come on man!")
            .case(Option.SOME(Any), do=lambda v: "Unaccounted for")
        )

        assert value() == expected


def test_match_records():
    """records can be pattern matched"""
    Color = record({"r": int, "g": int, "b": int, "a": int})
    User = record({"first": str, "last": str, "age": int})

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
            .case(Color(a=0), do=lambda v: f"r:{v.r}g:{v.g}b:{v.b}a:{v.a}")
            .case(Color(), do=lambda: "Not matched")
            .case(User(last="Doe"), do=lambda v: f"{v.first} {v.age}")
            .case(User(), do=lambda v: "Not matched")
        )

        assert value() == expected


def test_match_lists():
    """lists can be pattern matched"""
    test_data = [
        (l(2, 3, 56, 34), "90"),
        (l(2, 3, 56, 36), "59"),
        (l("foo", 6.0, 89), "bar"),
        (l("any string", 6.0, 89), "woo-hoo"),
        (l("foo", 6.0), "one foo"),
        (l(True, "foo", 6.0, 7), "True, foo, 6.0, 7"),
        (l(), "Empty"),
    ]
    element_sum = lambda arr: reduce(lambda a, b: a + b, arr, 0)

    # '...' is used to capture values to be used in the matching expression
    for arg, expected in test_data:
        value = (
            match(arg)
            .case(l(2, ..., 36), do=lambda rest: f"{element_sum(rest)}")
            .case(l(2, 3, ...), do=lambda rest: f"{element_sum(rest)}")
            .case(l("foo", 6.0), do=lambda: "one foo")
            .case(l("foo", 6.0, ...), do=lambda: "bar")
            .case(l(str, 6.0, ...), do=lambda: "woo-hoo")
            .case(l(...), do=lambda rest: ", ".join(rest.map(lambda x: f"{x}")))
            .case(l(), do=lambda: "Empty")
        )

        assert value() == expected
