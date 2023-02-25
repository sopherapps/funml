"""Common utility functions"""
from __future__ import annotations
import datetime
import string
import types
import typing
import random
from typing import Any, Tuple, List, Union


def is_type(value: Any, cls: Any) -> bool:
    """Checks whether the given value is of the given type.

    Note: For now, using Generics won't be type checked that well
    Also subscriptable types are not really being checked well
    """
    _type = cls
    if _type in (Any, ...):
        return True

    _type = extract_type(_type)
    try:
        return isinstance(value, _type) or value == _type
    except Exception as exp:
        raise exp


def extract_type(annotation: Any):
    """Extracts the actual type from an annotation"""
    if annotation in (typing.Any, Ellipsis):
        return object

    elif isinstance(annotation, typing._SpecialForm):
        return tuple([extract_type(arg) for arg in annotation.__args__])

    elif isinstance(annotation, typing._GenericAlias):
        origin = annotation.__origin__
        origin_name = getattr(origin, "_name", None)
        if origin_name == "Union":
            return tuple([extract_type(arg) for arg in annotation.__args__])
        else:
            return origin

    try:
        if isinstance(annotation, types.GenericAlias):
            return annotation.__origin__
    except AttributeError:
        pass

    return annotation


def right_pad_list(
    items: Union[List, Tuple], target_length: int, fill_value: Any
) -> List:
    """Right pads a given list or tuple to reach a given number of elements

    Args:
        items: the original list
        target_length: the final length of the padded list
        fill_value: the value to fill the empty slots in the padded list

    Returns:
        the new list with the given target length, or the old one if the target length is less than the original length
    """
    return list(items) + ([fill_value] * (target_length - len(items)))


def generate_random_string() -> str:
    """Generates a random string"""
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    random_string = "".join(random.choices(string.ascii_letters, k=8))
    return f"{random_string}{timestamp}"


def is_equal_or_of_type(val: Any, type_or_val: Any) -> bool:
    """Checks if the given value is equal or of the type given

    Ellipsis (...) or Any signifies any value
    """
    if type_or_val in (
        ...,
        Any,
    ):
        return True

    if val == type_or_val:
        return True

    try:
        if isinstance(val, type_or_val):
            return True
    except TypeError:
        return False

    return False


def equals(first: Any, other: Any) -> bool:
    """Checks for equality for values of any type.

    It is mainly here to handle special cases for
    types that funml has no control over, and yet
    don't have a funml-workable __eq__ implementation

    Args:
        first: the first value to check
        other: the other value to compare to `first`

    Returns:
        true if equal, false if not
    """
    if isinstance(first, (tuple, list)):
        return (
            type(first) == type(other)
            and len(first) == len(other)
            and all(equals(v1, v2) for v1, v2 in zip(first, other))
        )

    if isinstance(first, BaseException):
        return type(first) == type(other) and str(first) == str(other)

    return first == other
