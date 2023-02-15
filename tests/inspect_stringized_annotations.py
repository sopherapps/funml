"""Adapted from the standard lib: https://github.com/python/cpython/blob/main/Lib/test/inspect_stringized_annotations.py"""

from __future__ import annotations

a: int = 3
b: str = "foo"


class MyClass:
    a: int = 4
    b: str = "bar"
    c: tuple[str, ...] = ("boo",)

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __eq__(self, other):
        return (
            isinstance(other, MyClass)
            and self.a == other.a
            and self.b == other.b
            and self.c == other.c
        )


class UnannotatedClass:
    pass


class MyClassWithLocalAnnotations:
    mytype = int
    x: mytype
