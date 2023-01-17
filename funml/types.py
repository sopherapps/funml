"""All types used by funml"""
from typing import Any, Type, Union, Callable, Optional


class Assignment:
    """Class for making assignments"""

    def __init__(self, var: Any, t: Type = type(None)):
        self.__var = var
        self.__t = t
        self.__val = None

    def __le__(self, val: Any) -> "Assignment":
        """'<=' is the match operator. Here it is being used to assign a value."""
        if not isinstance(val, self.__t):
            raise TypeError(f"expected type {self.__t}, got {type(val)}")
        self.__val = val
        return self

    def __rshift__(self, nxt: Union["Expression", "Assignment", Callable]):
        """This makes piping using the '>>' symbol possible

        Combines with the given expression, assignments, Callables to produce a new expression
        where data flows from current to nxt
        """
        return _append_expn(self, nxt)

    def __iter__(self):
        """Generates an iterator that can be used to create a dict using dict()"""
        yield self.__var, self.__val

    def __call__(self) -> Any:
        """Returns the value associated with this assignment"""
        return self.__val


class Context(dict):
    """The _context map containing variables in scope"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__last_computed_val: Any = None

    def set_last_computed_val(self, val: Any):
        self.__last_computed_val = val

    @property
    def last_computed_val(self) -> Any:
        """The last computed value in the chain"""
        return self.__last_computed_val


class Expression:
    """Expressions which compute themselves and return an Assignment"""

    def __init__(self, f: Optional["Operation"] = None):
        self.__f = f if f is not None else lambda x: x
        self._context: "Context" = Context()

    def __call__(self, *args, **kwargs):
        """computes self and returns the value"""
        last_computed_val = self._context.last_computed_val

        if isinstance(last_computed_val, Context):
            self._context.update(last_computed_val)
            self._context.set_last_computed_val(None)
        elif last_computed_val is not None:
            return self.__f(last_computed_val, *args, **self._context, **kwargs)

        return self.__f(*args, **self._context, **kwargs)

    def __rshift__(self, nxt: Union["Expression", "Assignment", Callable]):
        """This makes piping using the '>>' symbol possible

        Combines with the given expression to produce a new expression
        where data flows from current to nxt
        """
        return _append_expn(self, nxt)

    def set_last_computed_val(self, val):
        """Sets the last computed value for the context of this expression

        Useful when passing the value through a series of expressions, from left to right
        """
        self._context.set_last_computed_val(val=val)


class Operation:
    """A computation"""

    def __init__(self, f: Callable):
        self.__f = f

    def __call__(self, *args: Any, **kwargs: "Context") -> Any:
        """Handles the actual computation"""
        return self.__f(*args, **kwargs)


def _to_expn(v: Union["Expression", "Assignment", Callable, Any]) -> "Expression":
    """Converts a Callable or Expression into an Expression"""
    if isinstance(v, Expression):
        return v
    elif isinstance(v, Assignment):
        return Expression(Operation(lambda: Context(**dict(v))))
    elif isinstance(v, Callable):
        return Expression(Operation(v))
    # return a noop expression
    return Expression(Operation(f=lambda: v))


def _append_expn(
    first: Union["Expression", "Assignment", Callable, Any],
    other: Union["Expression", "Assignment", Callable, Any],
):
    """Returns a new combined Expression where the current expression runs before the passed expression"""
    other = _to_expn(other)
    first = _to_expn(first)
    other.set_last_computed_val(first())
    return other
