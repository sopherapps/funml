"""A collection of ways to compose functions in a functional programming way"""
from functools import reduce
from typing import Callable, Optional, Union

from funml.assignments import _Assignment
from funml.context import _Context
from funml.operations import _Operation


def fn(*expressions: Union["_Expression", "_Assignment", Callable]) -> "_Expression":
    """Composes a new expression from other expression, moving from left to right"""
    return reduce(lambda a, b: _append(_to_expn(a), _to_expn(b)), expressions)


def _to_expn(v: Union["_Expression", "_Assignment", Callable]) -> "_Expression":
    """Converts a Callable or Expression into an Expression"""
    if isinstance(v, _Expression):
        return v
    elif isinstance(v, _Assignment):
        return _Expression(_Operation(lambda: _Context(**dict(v))))
    elif isinstance(v, Callable):
        return _Expression(_Operation(v))

    raise TypeError(f"expected a Callable, but got {type(v)}")


def _append(first: "_Expression", other: "_Expression"):
    """Returns a new combined Expression where the current expression runs before the passed expression"""
    other._context.set_last_computed_val(first())
    return other


class _Expression:
    """Expressions which compute themselves and return an Assignment"""

    def __init__(self, f: Optional["_Operation"] = None):
        self.__f = f if f is not None else lambda x: x
        self._context: "_Context" = _Context()

    def __call__(self, *args, **kwargs):
        """computes self and returns the value"""
        last_computed_val = self._context.last_computed_val

        if isinstance(last_computed_val, _Context):
            self._context.update(last_computed_val)
            self._context.set_last_computed_val(None)
        elif last_computed_val is not None:
            return self.__f(last_computed_val, *args, **self._context, **kwargs)

        return self.__f(*args, **self._context, **kwargs)

    def __rshift__(self, nxt: "_Expression"):
        """This makes piping using the '>>' symbol possible

        Combines with the given expression to produce a new expression
        where data flows from current to nxt
        """
        return _append(self, nxt)
