"""Common monads

For more about monads, https://en.wikipedia.org/wiki/Monad_(functional_programming)
"""
from typing import Any, Union, Callable

from .enum import Enum
from .. import match
from ..types import Assignment, Expression, to_expn, Operation


def if_ok(do: Union[Expression, Assignment, Callable, Any], strict=True) -> Expression:
    """Does the given operation if value passed to resulting expression is Result.OK.

    If the value is Result.ERR, it just returns the Result.ERR without
    doing anything about it.

    Args:
        do: The expression, function, assignment to run or value to return when Result.OK
        strict: if only Results should be expected

    Returns:
        An expression to run the `do` operation when value passed to expression is Result.OK
        or to just return the Result.ERR

    Raises:
        funml.errors.MatchError: value provided was not a Result and `strict` is True
    """
    routine = (
        match()
        .case(Result.OK(Any), do=to_expn(do))
        .case(Result.ERR(Exception), do=lambda v: Result.ERR(v))
    )

    if not strict:
        routine = routine.case(Any, do=lambda v: v)

    return Expression(Operation(routine))


def if_err(do: Union[Expression, Assignment, Callable, Any], strict=True) -> Expression:
    """Does the given operation if value passed to resulting expression is Result.ERR.

    If the value is Result.OK, it just returns the Result.OK without
    doing anything about it.

    Args:
        do: The expression, function, assignment to run or value to return when Result.ERR
        strict: if only Results should be expected

    Returns:
        An expression to run the `do` operation when value passed to expression is Result.ERR
        or to just return the Result.OK

    Raises:
        funml.errors.MatchError: value provided was not a Result if strict is True
    """
    routine = (
        match()
        .case(Result.OK(Any), do=lambda v: Result.OK(v))
        .case(Result.ERR(Exception), do=to_expn(do))
    )

    if not strict:
        routine = routine.case(Any, do=lambda v: v)

    return Expression(Operation(routine))


def if_some(
    do: Union[Expression, Assignment, Callable, Any], strict=True
) -> Expression:
    """Does the given operation if value passed to resulting expression is Option.SOME.

    If the value is Result.NONE, it just returns the Result.NONE without
    doing anything about it.

    Args:
        do: The expression, function, assignment to run or value to return when Option.SOME
        strict: if only Options should be expected

    Returns:
        An expression to run the `do` operation when value passed to expression is Option.SOME
        or to just return the Option.NONE

    Raises:
        funml.errors.MatchError: value provided was not an Option if strict is True
    """
    routine = (
        match()
        .case(Option.SOME(Any), do=to_expn(do))
        .case(Option.NONE, do=lambda: Option.NONE)
    )

    if not strict:
        routine = routine.case(Any, do=lambda v: v)

    return Expression(Operation(routine))


def if_none(
    do: Union[Expression, Assignment, Callable, Any], strict=True
) -> Expression:
    """Does the given operation if value passed to resulting expression is Option.NONE.

    If the value is Option.SOME, it just returns the Option.SOME without
    doing anything about it.

    Args:
        do: The expression, function, assignment to run or value to return when Option.NONE
        strict: if only Options should be expected

    Returns:
        An expression to run the `do` operation when value passed to expression is Option.NONE
        or to just return the Option.SOME

    Raises:
        funml.errors.MatchError: value provided was not an Option if strict is True
    """
    routine = (
        match()
        .case(Option.SOME(Any), do=lambda v: Option.SOME(v))
        .case(Option.NONE, do=to_expn(do))
    )

    if not strict:
        routine = routine.case(Any, do=lambda v: v)

    return Expression(Operation(routine))


def is_ok(v: "Result", strict=True) -> bool:
    """Checks if `v` is Result.OK.

    Args:
        v: The value to check
        strict: if value should be a Result

    Returns:
        True if `v` is a Result.OK else False

    Raises:
        funml.errors.MatchError: value provided was not a Result if strict is True
    """
    negative_pattern = Result.ERR(Exception) if strict else Any

    return (
        match()
        .case(Result.OK(Any), do=lambda: True)
        .case(negative_pattern, do=lambda: False)
    )(v)


def is_err(v: "Result", strict=True) -> bool:
    """Checks if `v` is Result.ERR.

    Args:
        v: The value to check
        strict: if value should be a Result

    Returns:
        True if `v` is a Result.ERR else False

    Raises:
        funml.errors.MatchError: value provided was not a Result if strict is True
    """
    negative_pattern = Result.OK(Any) if strict else Any

    return (
        match()
        .case(Result.ERR(Exception), do=lambda: True)
        .case(negative_pattern, do=lambda: False)
    )(v)


def is_some(v: "Option", strict=True) -> bool:
    """Checks if `v` is Option.SOME.

    Args:
        v: The value to check
        strict: if value should be a Option

    Returns:
        True if `v` is a Option.SOME else False

    Raises:
        funml.errors.MatchError: value provided was not an Option if strict is True
    """
    negative_pattern = Option.NONE if strict else Any

    return (
        match()
        .case(Option.SOME(Any), do=lambda: True)
        .case(negative_pattern, do=lambda: False)
    )(v)


def is_none(v: "Option", strict=True) -> bool:
    """Checks if `v` is Option.NONE.

    Args:
        v: The value to check
        strict: if value should be a Option

    Returns:
        True if `v` is a Option.NONE else False

    Raises:
        funml.errors.MatchError: value provided was not an Option if strict is True
    """
    negative_pattern = Option.SOME(Any) if strict else Any

    return (
        match()
        .case(Option.NONE, do=lambda: True)
        .case(negative_pattern, do=lambda: False)
    )(v)


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
