"""Common utility functions"""
import datetime
import functools
import re
import string
import sys
import types
import typing
import random
from typing import Any, Dict, Tuple, List, Set


_compound_type_regex = re.compile(r"tuple|list|set|dict")
_compound_type_generic_type_map = {
    "tuple": "Tuple",
    "dict": "Dict",
    "list": "List",
    "set": "Set",
}
_default_globals = {
    "Tuple": Tuple,
    "Dict": Dict,
    "Set": Set,
    "List": List,
}


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


def get_cls_annotations(cls, *, globals=None, locals=None, eval_str=False):
    """Compute the annotations dict for a class.
    Passing in an object of any other type raises TypeError.
    Returns a dict.  get_cls_annotations() returns a new dict every time
    it's called; calling it twice on the same object will return two
    different but equivalent dicts.
    This function handles several details for you:
      * If eval_str is true, values of type str will
        be un-stringized using eval().  This is intended
        for use with stringized annotations
        ("from __future__ import annotations").
      * If cls doesn't have an annotations dict, returns an
        empty dict.
      * Ignores inherited annotations on classes.  If a class
        doesn't have its own annotations dict, returns an empty dict.
      * All accesses to object members and dict values are done
        using getattr() and dict.get() for safety.
      * Always, always, always returns a freshly-created dict.
    eval_str controls whether or not values of type str are replaced
    with the result of calling eval() on those values:
      * If eval_str is true, eval() is called on values of type str.
      * If eval_str is false (the default), values of type str are unchanged.
    globals and locals are passed in to eval(); see the documentation
    for eval() for more information.  If either globals or locals is
    None, this function may replace that value with a context-specific
    default, contingent on type(cls):
      * globals defaults to
        sys.modules[cls.__module__].__dict__ and locals
        defaults to the obj class namespace.

    Adapted from the standard lib definition: https://github.com/python/cpython/blob/main/Lib/inspect.py
    """
    if isinstance(cls, type):
        # class
        obj_dict = getattr(cls, "__dict__", None)
        if obj_dict and hasattr(obj_dict, "get"):
            ann = obj_dict.get("__annotations__", None)
            if isinstance(ann, types.GetSetDescriptorType):
                ann = None
        else:
            ann = None

        obj_globals = _default_globals
        module_name = getattr(cls, "__module__", None)
        if module_name:
            module = sys.modules.get(module_name, None)
            if module:
                obj_globals.update(getattr(module, "__dict__", {}))
        obj_locals = dict(vars(cls))
        unwrap = cls
    else:
        raise TypeError(f"{cls!r} is not a class")

    if ann is None:
        return {}

    if not isinstance(ann, dict):
        raise ValueError(f"{cls!r}.__annotations__ is neither a dict nor None")

    if not ann:
        return {}

    if not eval_str:
        return dict(ann)

    if unwrap is not None:
        while True:
            if hasattr(unwrap, "__wrapped__"):
                unwrap = unwrap.__wrapped__
                continue
            if isinstance(unwrap, functools.partial):
                unwrap = unwrap.func
                continue
            break
        if hasattr(unwrap, "__globals__"):
            obj_globals = unwrap.__globals__

    if globals is None:
        globals = obj_globals
    if locals is None:
        locals = obj_locals

    return_value = {
        key: value
        if not isinstance(value, str)
        else eval(_to_generic(value), globals, locals)
        for key, value in ann.items()
    }
    return return_value


def get_cls_defaults(cls: type, annotations: Dict[str, type]) -> Dict[str, Any]:
    """Retrieves all default values of a class attributes.

    Args:
        cls: the class
        annotations: the annotations of the class

    Returns:
        a dictionary of attributes and their default values

    Raises:
        TypeError if the defaults provided are not of the expected type as specified in annotations
    """
    defaults = {}

    for attr, type_ in annotations.items():
        try:
            value = getattr(cls, attr)

            if not is_type(value, type_):
                raise TypeError(
                    f"attribute {attr} should be of type {type_}; got {value}"
                )

            defaults[attr] = value
        except AttributeError:
            pass

    return defaults


def _to_generic(annotation: str) -> str:
    """Converts a future annotation like list[str] to a generic annotation e.g. List[str]

    This is just for compatibility when it comes to python < 3.10
    """
    return _compound_type_regex.sub(
        lambda v: _compound_type_generic_type_map[v.string[v.start() : v.end()]],
        annotation,
    )
