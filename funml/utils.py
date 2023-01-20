"""Common utility functions"""
import typing
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

    return isinstance(value, _type)
