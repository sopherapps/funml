"""Common utility functions"""
import datetime
import string
import typing
import random
from typing import Any


def is_type(value: Any, cls: Any) -> bool:
    """Checks whether the given value is of the given type.

    Note: For now, using Generics won't be type checked that well
    Also subscriptable types are not really being checked well
    """
    _type = cls
    if _type in (Any,):
        return True

    if isinstance(_type, typing._SpecialForm):
        _type = _type.__args__

    if isinstance(_type, typing._GenericAlias):
        origin = getattr(_type, "__origin__")
        origin_name = getattr(origin, "_name", None)
        if origin_name == "Union":
            _type = _type.__args__
        else:
            _type = origin

    return isinstance(value, _type) or value == _type


def generate_random_string() -> str:
    """Generates a random string"""
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    random_string = "".join(random.choices(string.ascii_letters, k=8))
    return f"{random_string}{timestamp}"


def is_equal_or_of_type(val: Any, type_or_val: Any) -> bool:
    """Checks if the given value is equal or of the type given

    Ellipsis (...) signifies any value
    """
    if type_or_val is ...:
        return True

    if val == type_or_val:
        return True

    try:
        if isinstance(val, type_or_val):
            return True
    except TypeError:
        return False

    return False
