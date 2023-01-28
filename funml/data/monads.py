"""Common monads

For more about monads, https://en.wikipedia.org/wiki/Monad_(functional_programming)
"""
from typing import Any, Union, Callable

from .enum import Enum
from .. import match
from ..types import Assignment, Expression, to_expn, Operation


def if_ok(do: Union[Expression, Assignment, Callable, Any]) -> Expression:
    """Does the given operation if value passed to resulting expression is Result.OK.

    If the value is Result.ERR, it just returns the Result.ERR without
    doing anything about it.

    Args:
        do: The expression, function, assignment to run or value to return when Result.OK

    Returns:
        An expression to run the `do` operation when value passed to expression is Result.OK
        or to just return the Result.ERR

    Raises:
        funml.errors.MatchError: value provided was not a Result
    """
    op = Operation(
        match()
        .case(Result.OK(Any), do=to_expn(do))
        .case(Result.ERR(Exception), do=lambda v: Result.ERR(v))
    )
    return Expression(op)


def if_err(do: Union[Expression, Assignment, Callable, Any]) -> Expression:
    """Does the given operation if value passed to resulting expression is Result.ERR.

    If the value is Result.OK, it just returns the Result.OK without
    doing anything about it.

    Args:
        do: The expression, function, assignment to run or value to return when Result.ERR

    Returns:
        An expression to run the `do` operation when value passed to expression is Result.ERR
        or to just return the Result.OK

    Raises:
        funml.errors.MatchError: value provided was not a Result
    """
    op = Operation(
        match()
        .case(Result.OK(Any), do=lambda v: Result.OK(v))
        .case(Result.ERR(Exception), do=to_expn(do))
    )
    return Expression(op)


def if_some(do: Union[Expression, Assignment, Callable, Any]) -> Expression:
    """Does the given operation if value passed to resulting expression is Option.SOME.

    If the value is Result.NONE, it just returns the Result.NONE without
    doing anything about it.

    Args:
        do: The expression, function, assignment to run or value to return when Option.SOME

    Returns:
        An expression to run the `do` operation when value passed to expression is Option.SOME
        or to just return the Option.NONE

    Raises:
        funml.errors.MatchError: value provided was not an Option
    """
    op = Operation(
        match()
        .case(Option.SOME(Any), do=to_expn(do))
        .case(Option.NONE, do=lambda: Option.NONE)
    )
    return Expression(op)


def if_none(do: Union[Expression, Assignment, Callable, Any]) -> Expression:
    """Does the given operation if value passed to resulting expression is Option.NONE.

    If the value is Option.SOME, it just returns the Option.SOME without
    doing anything about it.

    Args:
        do: The expression, function, assignment to run or value to return when Option.NONE

    Returns:
        An expression to run the `do` operation when value passed to expression is Option.NONE
        or to just return the Option.SOME

    Raises:
        funml.errors.MatchError: value provided was not an Option
    """
    op = Operation(
        match()
        .case(Option.SOME(Any), do=lambda v: Option.SOME(v))
        .case(Option.NONE, do=to_expn(do))
    )
    return Expression(op)


class Option(Enum):
    """Represents a value that is potentially None

    Variants:
        - SOME: when an actual value exists
        - NONE: when there is no value

    Example Usage:

        ```python
        import funml as ml
        from typing import Any

        b = ml.Option.SOME(6)
        a = ml.Option.NONE
        extract_option = (ml.match()
                .case(ml.Option.SOME(Any), do=lambda v: v)
                .case(ml.Option.NONE, do=lambda: "nothing found"))
        extract_option(b)
        # returns 6
        extract_option(a)
        # returns 'nothing found'
        ```
    """

    NONE = None
    SOME = Any


class Result(Enum):
    """Represents a value that is potentially an exception

    Variants:
        - ERR: when an exception is raised
        - OK: when there is a real value

    Example:

        ```python
        import funml as ml
        from typing import Any

        b = ml.Result.OK(60)
        a = ml.Result.ERR(TypeError("some error"))
        extract_result = (ml.match()
                .case(ml.Result.OK(Any), do=lambda v: v)
                .case(ml.Result.ERR(Exception), do=lambda v: str(v)))
        extract_result(b)
        # returns 60
        extract_result(a)
        # returns 'some error'
        ```
    """

    ERR = Exception
    OK = Any
