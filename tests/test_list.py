from typing import Any

import pytest

from funml import l, imap, ifilter, ireduce, to_json, from_json
from funml.data.lists import IList
from tests import conftest


def test_list_creation():
    """l creates an immutable IList"""
    test_data = [
        [2, 3, 56],
        ["foo", 6.0],
        [True, "foo", 6.0, 7],
    ]

    for v in test_data:
        assert list(l(*v)) == v


def test_list_concatenation():
    """concatenation of lists is done by `+`"""
    test_data = [
        ([2, 3, 56], ["foo", 6.0]),
        (["foo", 6.0], [2, 3, 56]),
        ([True, "foo", 6.0, 7], [2, 3, 56]),
    ]

    for v1, v2 in test_data:
        assert list(l(*v1) + l(*v2)) == [*v1, *v2]


def test_imap():
    """imap transforms each element of the list by the given transform"""
    test_data = [
        ([2, 3, 5], lambda x: x**2, l(4, 9, 25)),
        (["foo", 6.0], lambda x: f"{x}", l("foo", "6.0")),
        ([True, -6.0, 7], lambda x: x > 0, l(True, False, True)),
    ]

    for args, func, expected in test_data:
        transform = imap(func)
        assert transform(args) == expected


def test_ifilter():
    """ifilter returns only the items that fulfil a given test"""
    test_data = [
        ([2, 3, 5], lambda x: x % 2 != 0, l(3, 5)),
        (["foo", 6.0], lambda x: isinstance(x, str), l("foo")),
        ([True, -6.0, 7], lambda x: x > 0, l(True, 7)),
    ]

    for args, func, expected in test_data:
        sieve = ifilter(func)
        assert sieve(args) == expected


def test_ireduce():
    """ireduce reduces a sequence to single value using the function and initial value"""
    test_data = [
        ([2, 3, 5], lambda x, y: x + y, 6, 16),
        ([2, 3, 5], lambda x, y: x + y, None, 10),
        (["foo", 6.0], lambda x, y: f"{x}, {y}", None, "foo, 6.0"),
        (["foo", 6.0], lambda x, y: f"{x}; {y}", "list", "list; foo; 6.0"),
    ]

    for args, func, initial, expected in test_data:
        merger = ireduce(func, initial)
        assert merger(args) == expected


def test_head():
    """head returns the first element of the list"""
    test_data = [
        (l(2, 3, 5), 2),
        (l("foo", 6.0), "foo"),
        (l(True, -6.0, 7), True),
    ]

    for item, expected in test_data:
        assert item.head == expected


def test_tail():
    """tail returns the list (IList) of items except the first"""
    test_data = [
        (l(2, 3, 5), l(3, 5)),
        (l("foo", 6.0), l(6.0)),
        (l(True, -6.0, 7), l(-6.0, 7)),
    ]

    for item, expected in test_data:
        assert item.tail == expected


def test_to_json():
    """to_json method transforms list into a JSON string representation of list"""
    test_data = [
        (l(2, 3, 5), "[2, 3, 5]"),
        (l("foo", 6.0), '["foo", 6.0]'),
        (l(True, -6.0, 7), "[true, -6.0, 7]"),
        (
            l(
                True,
                conftest.Color(r=8, g=4, b=78, a=[conftest.Alpha.OPAQUE]),
                conftest.Color(r=55, g=40, b=9, a=[conftest.Alpha.TRANSLUCENT(0.4)]),
            ),
            (
                "["
                "true, "
                '{"r": 8, "g": 4, "b": 78, "a": ["Alpha.OPAQUE: \\"OPAQUE\\""]}, '
                '{"r": 55, "g": 40, "b": 9, "a": ["Alpha.TRANSLUCENT: 0.4"]}'
                "]"
            ),
        ),
        (
            l(
                True,
                conftest.Student(
                    name="John Doe",
                    favorite_color=conftest.Color(
                        r=8, g=4, b=78, a=[conftest.Alpha.OPAQUE]
                    ),
                ),
                conftest.Student(
                    name="Jane Doe",
                    favorite_color=conftest.Color(
                        r=55, g=40, b=9, a=[conftest.Alpha.TRANSLUCENT(0.4)]
                    ),
                ),
            ),
            (
                "["
                "true, "
                '{"name": "John Doe", "favorite_color": {"r": 8, "g": 4, "b": 78, "a": ["Alpha.OPAQUE: \\"OPAQUE\\""]}}, '
                '{"name": "Jane Doe", "favorite_color": {"r": 55, "g": 40, "b": 9, "a": ["Alpha.TRANSLUCENT: 0.4"]}}'
                "]"
            ),
        ),
    ]

    for item, expected in test_data:
        assert to_json(item) == expected


def test_from_json_strict():
    """from_json with strict transforms a JSON string representation into an IList of given annotation"""

    test_data = [
        ("[2, 3, 5]", IList[Any], l(2, 3, 5)),
        (
            (
                "["
                '{"r": 8, "g": 4, "b": 78, "a": ["Alpha.OPAQUE: \\"OPAQUE\\""]}, '
                '{"r": 55, "g": 40, "b": 9, "a": ["Alpha.TRANSLUCENT: 0.4"]}'
                "]"
            ),
            IList[conftest.Color],
            l(
                conftest.Color(r=8, g=4, b=78, a=[conftest.Alpha.OPAQUE]),
                conftest.Color(r=55, g=40, b=9, a=[conftest.Alpha.TRANSLUCENT(0.4)]),
            ),
        ),
        (
            (
                "["
                '{"name": "John Doe", "favorite_color": {"r": 8, "g": 4, "b": 78, "a": ["Alpha.OPAQUE: \\"OPAQUE\\""]}}, '
                '{"name": "Jane Doe", "favorite_color": {"r": 55, "g": 40, "b": 9, "a": ["Alpha.TRANSLUCENT: 0.4"]}}'
                "]"
            ),
            IList[conftest.Student],
            l(
                conftest.Student(
                    name="John Doe",
                    favorite_color=conftest.Color(
                        r=8, g=4, b=78, a=[conftest.Alpha.OPAQUE]
                    ),
                ),
                conftest.Student(
                    name="Jane Doe",
                    favorite_color=conftest.Color(
                        r=55, g=40, b=9, a=[conftest.Alpha.TRANSLUCENT(0.4)]
                    ),
                ),
            ),
        ),
    ]

    for item, type_, expected in test_data:
        got = from_json(type_=type_, value=item)
        assert got == expected


def test_from_json_not_strict():
    """from_json with not strict attempts to transform each item in a JSON string IList representation to the given annotation,
    defaulting to the expected JSON.loads output on error"""

    test_data = [
        ('["foo", 6.0]', IList[int], l("foo", 6)),
        ("[true, -6.0, 7]", IList[int], l(1, -6, 7)),
        (
            (
                "["
                "true, "
                '{"r": 8, "g": 4, "b": 78, "a": ["Alpha.OPAQUE: \\"OPAQUE\\""]}, '
                '{"r": 55, "g": 40, "b": 9, "a": ["Alpha.TRANSLUCENT: 0.4"]}'
                "]"
            ),
            IList[conftest.Color],
            l(
                True,
                conftest.Color(r=8, g=4, b=78, a=[conftest.Alpha.OPAQUE]),
                conftest.Color(r=55, g=40, b=9, a=[conftest.Alpha.TRANSLUCENT(0.4)]),
            ),
        ),
        (
            (
                "["
                '{"name": "John Doe", "favorite_color": {"r": 8, "g": 4, "b": 78, "a": ["Alpha.OPAQUE: \\"OPAQUE\\""]}}, '
                '"foo", '
                '{"name": "Jane Doe", "favorite_color": {"r": 55, "g": 40, "b": 9, "a": ["Alpha.TRANSLUCENT: 0.4"]}}'
                "]"
            ),
            IList[conftest.Student],
            l(
                conftest.Student(
                    name="John Doe",
                    favorite_color=conftest.Color(
                        r=8, g=4, b=78, a=[conftest.Alpha.OPAQUE]
                    ),
                ),
                "foo",
                conftest.Student(
                    name="Jane Doe",
                    favorite_color=conftest.Color(
                        r=55, g=40, b=9, a=[conftest.Alpha.TRANSLUCENT(0.4)]
                    ),
                ),
            ),
        ),
    ]

    for item, type_, expected in test_data:
        assert from_json(type_=type_, value=item, strict=False) == expected

        with pytest.raises(
            ValueError, match=r".* value .* should be of type: .*, got .*"
        ):
            from_json(type_=type_, value=item)
