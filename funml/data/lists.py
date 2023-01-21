"""lists that support functional programming concepts easily

Usage
---

# assignment

>> list1 = l(9, 7, 0)

# prepending data (immutably) i.e. new list is got

>> value = l(5, 6) + list1

# appending data (immutably) i.e. new list is got

>> value = list1 + l(7, 9)

# deleting data (immutably) i.e. new list is got
>> value = list1.filter(lambda v: v > 9)

# transforming data (immutably) i.e. new list is got
>> value = list1.map(lambda v: v + 9)

# destructuring list: the last argument gets all remaining items as one list
>> let(int, l(v, y, others)) <= list1

# iterating data
>> loop = fn(match(v)
            | l() <= fn()
            | l(head, tail) <= fn(
                                 lambda head: print(head),
                                 loop(tail),
                                 )
"""
from typing import Any, Optional, Callable


def l(*args: Any) -> "IList":
    """Creates an immutable list"""
    return IList(*args)


class IList:
    def __init__(self, *args: Any):
        prev: Optional[Node] = None
        for v in reversed(args):
            node = Node(_data=v, _next=prev)
            prev = node

        self.head: Optional["Node"] = prev
        self.size = len(args)

    def __len__(self):
        return self.size

    def __iter__(self):
        if self.head is None:
            return False

        yield self.head.value

        curr = self.head.next
        while curr is not None:
            yield curr.value
            curr = curr.next

    def __add__(self, other):
        if not isinstance(other, IList):
            return TypeError(
                f"add operation requires value to be of type IList, not {type(other)}"
            )

        return IList(*self, *other)

    def map(self, func: Callable):
        """Transforms each item of the list using the given function f"""
        return IList(*[func(v) for v in self])

    def filter(self, func: Callable):
        """Returns only items that return true when f is called on them"""
        return IList(*filter(func, self))


class Node:
    __slots__ = ["_data", "_next"]

    def __init__(self, _data: Any, _next: Optional["Node"] = None):
        self._data = _data
        self._next = _next

    @property
    def value(self):
        return self._data

    @property
    def next(self):
        return self._next

    def __lt__(self, other):
        return self._data < other.value

    def __le__(self, other):
        return self._data <= other.value

    def __eq__(self, other):
        return self._data == other.value

    def __gt__(self, other):
        return self._data > other.value

    def __ge__(self, other):
        return self._data >= other.value

    def __repr__(self):
        return self.value.__repr__()
