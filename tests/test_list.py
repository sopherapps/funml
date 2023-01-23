from funml import l


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


def test_list_map():
    """map transforms each element of the list by the given transform"""
    test_data = [
        ([2, 3, 5], lambda x: x**2, [4, 9, 25]),
        (["foo", 6.0], lambda x: f"{x}", ["foo", "6.0"]),
        ([True, -6.0, 7], lambda x: x > 0, [True, False, True]),
    ]

    for args, func, expected in test_data:
        assert list(l(*args).map(func)) == expected


def test_list_filter():
    """filter returns only the items that fulfil a given test"""
    test_data = [
        ([2, 3, 5], lambda x: x % 2 != 0, [3, 5]),
        (["foo", 6.0], lambda x: isinstance(x, str), ["foo"]),
        ([True, -6.0, 7], lambda x: x > 0, [True, 7]),
    ]

    for args, func, expected in test_data:
        assert list(l(*args).filter(func)) == expected


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
    """tail lazily returns (as a generator) the list of items except the first"""
    test_data = [
        (l(2, 3, 5), l(3, 5)),
        (l("foo", 6.0), l(6.0)),
        (l(True, -6.0, 7), l(-6.0, 7)),
    ]

    for item, expected in test_data:
        # got = list(item.tail)
        assert item.tail == expected
