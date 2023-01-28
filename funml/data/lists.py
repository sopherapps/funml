"""Immutable lists for ML functionality.

Typical Usage:

    ```python
    import funml as ml


    # initialize
    list1 = ml.l(9, 7, 0)

    # concatenate immutably
    value = ml.l(5, 6) + list1

    # deleting data (immutably) i.e. new list is got
    up_to_9_filter = ml.ifilter(lambda v: v < 9)
    value = up_to_9_filter(list1)

    # transforming data (immutably) i.e. new list is got
    add_9_transform = ml.imap(lambda v: v + 9)
    value = add_9_transform(list1)

    # iterating data using head and
    def print_head(v: ml.data.lists.IList) -> ml.data.lists.IList:
        print(v.head)
        return v.tail

    ml_print_head = ml.val(print_head)
    loop = (
            ml.match()
                .case(ml.l(), do=ml.val(None))
                .case(ml.l(...), do=lambda v: (ml_print_head >> loop)(v))
    )
    ```
"""
from functools import reduce
from typing import Any, Optional, Callable, List, Tuple, Union

from funml import types, utils
from funml.types import Expression, Operation


def l(*args: Any) -> "IList":
    """Creates an immutable list of any type of items.

    Creates a list of items of any type, that cannot be changed
    once created. It can only be used to create other lists, using methods on it like

    - [`+`][funml.data.lists.IList.__add__] - to combine two separate lists into a new one containing elements of both
    - [`imap(fn)`][funml.imap] - to create a new list with each element transformed according to the given function `fn`
    - [`filter(fn)`][funml.ifilter] - to return a new list containing only elements that conform to the given function `fn`

    Args:
        args: the items that make up the list

    Returns:
        An immutable list, [`IList][funml.data.lists.IList], containing the items passed to it.

    Example:
        ```python
        import funml as ml

        items = ml.l(120, 13, 40, 60, "hey", "men")

        num_filter = ml.ifilter(lambda x: isinstance(x, (int, float)))
        str_filter = ml.ifilter(lambda x: isinstance(x, str))
        nums = num_filter(items)
        strings = str_filter(items)

        double_transform = ml.imap(lambda x: x*2)
        doubled_nums = double_transform(nums)

        aggregator = ml.ireduce(lambda x, y: f"{x}, {y}")
        list_as_str = aggregator(items)

        print(nums)
        # prints [120, 13, 40, 60]

        print(strings)
        # prints ["hey", "men"]

        print(doubled_nums)
        # prints [240, 26, 80, 120]

        print(list_as_str)
        # prints '120, 13, 40, 60, hey, men'
        ```
    """
    return IList(*args)


def imap(func: Callable[[Any], Any]) -> Expression:
    """Creates an expression to transform each item by the given function.

    Expressions can be computed lazily at any time.

    Args:
        func: the function to use to transform each item

    Returns:
            A new IList with each item in data transformed according to the `func` function.
    """
    op = Operation(lambda data: IList(*[func(v) for v in data]))
    return Expression(op)


def ifilter(func: Callable[[Any], Any]) -> Expression:
    """Creates an expression to transform each item by the given function.

    Expressions can be computed lazily at any time.

    Args:
        func: the function to use to check if item should remain or be ignored.

    Returns:
        A new iList with only the items of data that returned true when `func` was called on them.
    """
    op = Operation(lambda data: IList(*filter(func, data)))
    return Expression(op)


def ireduce(
    func: Callable[[Any, Any], Any], initial: Optional[Any] = None
) -> Expression:
    """Creates an expression to reduce a sequence into one value using the given `func`.

    Expressions can be computed lazily at any time.

    Args:
        func: the function to reduce the sequence into a single value.
        initial: the initial value that acts like a default when sequence is empty,
                and is added onto by `func` when sequence has some items.

    Returns:
        A single item got from calling `func` repeatedly across the sequence for every
        two adjacent items.
    """
    if initial is None:
        op = Operation(lambda data: reduce(func, data))
    else:
        op = Operation(lambda data: reduce(func, data, initial))
    return Expression(op)


class IList(types.MLType):
    """An immutable list of items of any type.

    Args:
        args: the items to be included in the list.
    """

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
    def head(self) -> Any:
        """The first item in the list."""
        return self._head.value

    @property
    def tail(self) -> "IList":
        """A new slice of the list containing all items except the first."""
        return IList.__from_node(self._head.next)

    def generate_case(self, do: types.Operation):
        """See Base class: [`MLType`][funml.types.MLType]"""
        start = 0 if self.__capture_start is None else self.__capture_start
        tail_len = self.__capture_tail_len

        def op(arg):
            arg_slice = arg[start : (len(arg) - tail_len)]
            return do(arg_slice)

        return self._is_like, types.Expression(types.Operation(func=op))

    def _is_like(self, other: Any) -> bool:
        """See Base Class: [`MLType`][funml.types.MLType]"""
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
        """The number of items in the list."""
        if self.__size is None:
            self.__size = len(self._self_list)
        return self.__size

    @property
    def _self_list(self):
        """A cache of the native list that corresponds to this list."""
        if self.__list is None:
            self.__list = list(self.__iter__())
        return self.__list

    @property
    def _pre_capture(self):
        """A slice of the list pattern before the section to be captured when matching."""
        if self.__pre_capture is None and self.__capture_start is not None:
            self.__pre_capture = self._self_list[: self.__capture_start]
        return self.__pre_capture

    @property
    def _post_capture(self):
        """A slice of the list pattern after the section to be captured when matching."""
        if self.__post_capture is None:
            self.__post_capture = self._self_list[
                (self._size - self.__capture_tail_len) :
            ]
        return self.__post_capture

    @classmethod
    def __from_node(cls, head: "_Node") -> "IList":
        """Generates a slice of the old IList given one node of that list.

        In this case, the new list shares the same memory as the old list
        so don't use this in scenarios where immutable lists are needed.

        Args:
            head: the node from which the new list is to start from.

        Returns:
            A new list that shares memory with the old list. **NOTE: This is not immutable. Don't use it**.
        """
        i_list = IList()
        i_list._head = head
        return i_list

    def __set_size_from_args(self, args: Tuple[Any]):
        """Updates the size of this list basing on the args passed.

        Args:
            args: the items to be put in this list.
        """
        args_len = len(args)
        if args_len > 0:
            self.__size = args_len

    def __initialize_from_tuple(self, args: Tuple[Any]):
        """Initializes the list using items passed to it as a tuple.

        Initializes the current IList, generating nodes corresponding to the args passed
        and setting any capture sections if `...` is found.

        Args:
            args: the items to include in the list
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
        """Computes the length of the list."""
        return self._size

    def __iter__(self):
        """Makes the list an iterable."""
        if self._head is None:
            return

        yield self._head.value

        curr = self._head.next
        while curr is not None:
            yield curr.value
            curr = curr.next

    def __add__(self, other: Any) -> "IList":
        """Creates a new list with the current list and the `other` list merged.

        Args:
            other: the list to be appended to current list when creating new merged list.

        Returns:
            A new list which is a combination of the current list and the `other` list.

        Raises:
            TypeError: other is not an `IList`
        """
        if not isinstance(other, IList):
            raise TypeError(
                f"add operation requires value to be of type IList, not {type(other)}"
            )

        return IList(*self, *other)

    def __getitem__(self, item: Union[slice, int]) -> Union["IList", Any]:
        """Makes this list subscriptable and sliceable.

        Args:
            item: the index or slice to return.

        Returns:
            An `IList` if `index` was a slice or an item in the list if index was an integer.

        Raises:
            IndexError: if `item` is out of range of the list.
        """
        if isinstance(item, slice):
            return IList(*self._self_list[item])
        return self._self_list[item]

    def __eq__(self, other: Any) -> bool:
        """Checks equality of the this list and `other`.

        Args:
            other: the value to compare with current list.
        """
        return utils.equals(self._self_list, other._self_list)

    def __str__(self):
        """Generates a readable presentation of the list."""
        map_to_str = imap(str)
        return f"[{', '.join(map_to_str(self))}]"


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
        if not utils.is_equal_or_of_type(val, type_or_val=type_or_val):
            return False

    return True
