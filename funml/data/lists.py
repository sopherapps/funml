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

# iterating data using head and tail
>> loop = (fn(match(v)
            .case(l(), do= fn())
            .case(l(...), do= fn(
                                 lambda rest: print(rest.head),
                                 loop(rest.tail),
                                 ))
"""
from typing import Any, Optional, Callable, List, Tuple

from funml import types


def l(*args: Any) -> "IList":
    """Creates an immutable list"""
    return IList(*args)


class IList(types.MLType):
    def __init__(self, *args: Any):
        self.__size: Optional[int] = None
        self.__capture_start: Optional[int] = None
        self.__capture_tail_len: int = 0
        self.__pre_capture: Optional[List[Any]] = None
        self.__post_capture: Optional[List[Any]] = None
        self.__list: Optional[List[Any]] = None
        self._head: Optional["_Node"] = None

        self.__set_size_from_args(args)
        self.__initialize_from_tuple(args)

    @property
    def head(self):
        return self._head.value

    @property
    def tail(self):
        return IList.__from_node(self._head.next)

    def map(self, func: Callable):
        """Transforms each item of the list using the given function f"""
        return IList(*[func(v) for v in self])

    def filter(self, func: Callable):
        """Returns only items that return true when f is called on them"""
        return IList(*filter(func, self))

    def generate_case(self, do: types.Operation):
        """Generates a case statement for pattern matching"""
        start = 0 if self.__capture_start is None else self.__capture_start
        tail_len = self.__capture_tail_len

        def op(arg):
            arg_slice = arg[start : (len(arg) - tail_len)]
            return do(arg_slice)

        return self._is_like, types.Expression(types.Operation(func=op))

    def _is_like(self, other):
        """Checks that a value has the given pattern"""
        if not isinstance(other, IList):
            return False

        if self._size > other._size:
            return False

        if self.__capture_start is None:
            return self == other

        pre_capture = other._self_list[: self.__capture_start]
        post_capture = other._self_list[(len(other) - self.__capture_tail_len) :]

        return _lists_match(
            schema=self._pre_capture, actual=pre_capture
        ) and _lists_match(schema=self._post_capture, actual=post_capture)

    @property
    def _size(self):
        if self.__size is None:
            self.__size = len(self._self_list)
        return self.__size

    @property
    def _self_list(self):
        if self.__list is None:
            self.__list = list(self.__iter__())
        return self.__list

    @property
    def _pre_capture(self):
        if self.__pre_capture is None and self.__capture_start is not None:
            self.__pre_capture = self._self_list[: self.__capture_start]
        return self.__pre_capture

    @property
    def _post_capture(self):
        if self.__post_capture is None:
            self.__post_capture = self._self_list[
                (self._size - self.__capture_tail_len) :
            ]
        return self.__post_capture

    @classmethod
    def __from_node(cls, head: "_Node"):
        """Generates a slice of the old IList given one node of that list

        In this case, the new list shares the same memory as the old list
        so don't use this in scenarios where immutable lists are needed.
        """
        i_list = IList()
        i_list._head = head
        return i_list

    def __set_size_from_args(self, args: Tuple[Any]):
        """Computest the size of the new IList if args are passed to the init"""
        args_len = len(args)
        if args_len > 0:
            self.__size = args_len

    def __initialize_from_tuple(self, args: Tuple[Any]):
        """
        Initializes the current IList, generating nodes corresponding to the args passed
        and setting any capture sections if `...` is found
        """
        prev: Optional[_Node] = None
        for i, v in enumerate(reversed(args)):
            node = _Node(_data=v, _next=prev)
            prev = node

            if v is ...:
                self.__capture_start = self._size - i - 1
                self.__capture_tail_len = i

        self._head: Optional["_Node"] = prev

    def __len__(self):
        return self._size

    def __iter__(self):
        if self._head is None:
            return

        yield self._head.value

        curr = self._head.next
        while curr is not None:
            yield curr.value
            curr = curr.next

    def __add__(self, other):
        if not isinstance(other, IList):
            return TypeError(
                f"add operation requires value to be of type IList, not {type(other)}"
            )

        return IList(*self, *other)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return IList(*self._self_list[item])
        return self._self_list[item]

    def __eq__(self, other):
        return self._self_list == other._self_list


class _Node:
    __slots__ = ["_data", "_next"]

    def __init__(self, _data: Any, _next: Optional["_Node"] = None):
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


def _lists_match(schema: List[Any], actual: List[Any]):
    """Matches two builtin lists"""
    if schema == actual:
        # try the simple probably optimised version
        return True

    if not isinstance(schema, list):
        raise TypeError(f"must be list, got {type(schema)}")

    if not isinstance(actual, list):
        raise TypeError(f"must be list, got {type(actual)}")

    if len(schema) != len(actual):
        return False

    for type_or_val, val in zip(schema, actual):
        if val == type_or_val:
            continue

        try:
            if isinstance(val, type_or_val):
                continue
        except TypeError:
            return False

        return False

    return True
