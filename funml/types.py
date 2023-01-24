"""All types used by funml"""
from inspect import signature
from typing import Any, Type, Union, Callable, Optional, List, Tuple

from funml import errors


class Assignment:
    """Class for making assignments"""

    def __init__(self, var: Any, t: Type = type(None), val: Any = None):
        self.__var = var
        self.__t = t

        if not isinstance(val, t):
            raise TypeError(f"expected type {t}, got {type(val)}")

        self.__val = val

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


class MLType:
    """The base type for all ML-enabled types like records, enums etc."""

    def generate_case(self, expn: "Expression"):
        """Generates a case statement for pattern matching"""
        raise NotImplemented("generate case not implemented")


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


class MatchExpression(Expression):
    """Expression used when matching"""

    def __init__(self, arg: Any):
        super().__init__(f=Operation(self))
        self._matches: List[Tuple[Callable, Expression]] = []
        self.__arg = arg

    def case(self, obj: MLType, do: Expression):
        """adds a case to a match statement"""
        check, expn = obj.generate_case(do)
        self.__add_match(check=check, expn=expn)
        return self

    def __add_match(self, check: Callable, expn: Expression):
        """Adds a match to the list of matches"""
        if not callable(check):
            raise TypeError(f"the check is supposed to be a callable. Got {check}")

        if not isinstance(expn, Expression):
            raise TypeError(
                f"expected expression to be an Expression. Got {type(expn)}"
            )

        self._matches.append((check, expn))

    def __call__(self):
        """This class transforms into a conditional callable"""
        arg = self.__arg

        for check, expn in self._matches:
            if check(arg):
                return expn(arg)

        raise errors.MatchError(arg)


class Operation:
    """A computation"""

    def __init__(self, func: Callable):
        sig = _get_func_signature(func)
        if len(sig.parameters) == 0:
            # be more fault tolerant by using variable params
            self.__f = lambda *args: func()
        else:
            self.__f = func

    def __call__(self, *args: Any, **kwargs: "Context") -> Any:
        """Handles the actual computation"""
        return self.__f(*args, **kwargs)


def _get_func_signature(func: Callable):
    """Gets the function signature of the given callable"""
    try:
        return signature(func)
    except ValueError:
        return signature(func.__call__)


def _to_expn(v: Union["Expression", "Assignment", Callable, Any]) -> "Expression":
    """Converts a Callable or Expression into an Expression"""
    if isinstance(v, Expression):
        return v
    elif isinstance(v, Assignment):
        return Expression(Operation(lambda: Context(**dict(v))))
    elif isinstance(v, Callable):
        return Expression(Operation(v))
    # return a noop expression
    return Expression(Operation(func=lambda: v))


def _append_expn(
    first: Union["Expression", "Assignment", Callable, Any],
    other: Union["Expression", "Assignment", Callable, Any],
):
    """Returns a new combined Expression where the current expression runs before the passed expression"""
    other = _to_expn(other)
    first = _to_expn(first)
    other.set_last_computed_val(first())
    return other
