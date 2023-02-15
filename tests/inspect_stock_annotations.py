"""Adapted from the standard lib: https://github.com/python/cpython/blob/main/Lib/test/inspect_stock_annotations.py"""
a: int = 3
b: str = "foo"


class MyClass:
    a: int = 4
    b: str = "bar"

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return isinstance(other, MyClass) and self.a == other.a and self.b == other.b


class UnannotatedClass:
    pass
