"""All types used by funml"""
from inspect import signature
from typing import Any, Type, Union, Callable, Optional, List, Tuple

from funml import errors
from funml.utils import is_equal_or_of_type


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


class MLType:
    """The base type for all ML-enabled types like records, enums etc."""

    def generate_case(self, do: "Operation"):
        """Generates a case statement for pattern matching"""
        raise NotImplemented("generate case not implemented")


class Expression:
    """Expressions which compute themselves and return an Assignment"""

    def __init__(self, f: Optional["Operation"] = None):
        self._f = f if f is not None else lambda x: x
        self._context: "Context" = Context()
        self._queue: List[Expression] = []

    def __call__(self, *args, **kwargs):
        """computes self and returns the value"""
        prev_output = self._run_prev_expns(*args, **kwargs)

        if isinstance(prev_output, Context):
            self._context.update(prev_output)
        elif prev_output is not None:
            return self._f(prev_output, *args, **self._context, **kwargs)

        return self._f(*args, **self._context, **kwargs)

    def __rshift__(self, nxt: Union["Expression", "Assignment", Callable]):
        """This makes piping using the '>>' symbol possible

        Combines with the given expression to produce a new expression
        where data flows from current to nxt
        """
        return _append_expn(self, nxt)

    def _run_prev_expns(self, *args, **kwargs) -> Union["Context", Any]:
        """Runs all the previous expressions, returning the final output"""
        output = None

        for expn in self._queue:
            if output is None:
                output = expn(*args, **expn._context, **kwargs)
            elif isinstance(output, Context):
                output = expn(*args, **expn._context, **output, **kwargs)
            else:
                output = expn(output, *args, **expn._context, **kwargs)

        return output

    def append_prev_expns(self, *expns: "Expression"):
        """Appends expressions that should be computed before this one"""
        self._queue += expns

    def clear_prev_expns(self):
        """Clears all previous expressions in queue"""
        self._queue.clear()


class MatchExpression(Expression):
    """Expression used when matching"""

    def __init__(self, arg: Optional[Any] = None):
        super().__init__(f=Operation(self))
        self._matches: List[Tuple[Callable, Expression]] = []
        self.__arg = arg

    def case(self, obj: Union[MLType, Any], do: Callable):
        """adds a case to a match statement"""
        if isinstance(obj, MLType):
            check, expn = obj.generate_case(Operation(func=do))
        else:
            check = lambda arg: is_equal_or_of_type(arg, obj)
            expn = Expression(Operation(func=do))

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

    def __call__(self, arg: Optional[Any] = None):
        """This class transforms into a conditional callable"""
        if arg is None:
            arg = self.__arg

        args = [] if arg is None else [arg]
        prev_output = self._run_prev_expns(*args)
        if prev_output is not None:
            arg = prev_output

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
        # update the context
        return Expression(Operation(lambda **kwargs: Context(**kwargs, **dict(v))))
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

    other.append_prev_expns(*first._queue, first)
    first.clear_prev_expns()
    return other
