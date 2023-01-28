from funml import l, imap, ifilter, ireduce


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
