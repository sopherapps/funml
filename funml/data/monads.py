"""Common monads

For more about monads, https://en.wikipedia.org/wiki/Monad_(functional_programming)
"""
from typing import Any, Union, Callable

from .enum import Enum
from .. import match
from ..types import Expression, to_expn, Operation


def if_ok(do: Union[Expression, Callable, Any], strict: bool = True) -> Expression:
    """Does the given operation if value passed to resulting expression is Result.OK.

    If the value is Result.ERR, it just returns the Result.ERR without
    doing anything about it.

    Args:
        do: The expression, function to run or value to return when Result.OK
        strict: if only Results should be expected

    Example:
        ```python
        import funml as ml

        ok_value = ml.Result.OK(90)
        err_value = ml.Result.ERR(TypeError("some stuff"))
        another_value = None

        # in case the value may not be a Result, set strict to False
        print(ml.if_ok(str, strict=False)(another_value))
        # prints None

        ok_to_str = ml.if_ok(str)
        print(ok_to_str(err_value))
        # prints <Result.ERR: (TypeError('some stuff'),)>

        print(ok_to_str(ok_value))
        # prints 90
        ```

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


def if_err(do: Union[Expression, Callable, Any], strict: bool = True) -> Expression:
    """Does the given operation if value passed to resulting expression is Result.ERR.

    If the value is Result.OK, it just returns the Result.OK without
    doing anything about it.

    Args:
        do: The expression, function, to run or value to return when Result.ERR
        strict: if only Results should be expected

    Example:
        ```python
        import funml as ml

        ok_value = ml.Result.OK(90)
        err_value = ml.Result.ERR(TypeError("some stuff"))
        another_value = None

        # in case the value may not be a Result, set strict to False
        print(ml.if_err(str, strict=False)(another_value))
        # prints None

        err_to_str = ml.if_err(str)
        print(err_to_str(err_value))
        # prints 'some stuff'

        print(err_to_str(ok_value))
        # prints <Result.OK: ('90',)>
        ```

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


def if_some(do: Union[Expression, Callable, Any], strict: bool = True) -> Expression:
    """Does the given operation if value passed to resulting expression is Option.SOME.

    If the value is Result.NONE, it just returns the Result.NONE without
    doing anything about it.

    Args:
        do: The expression, function, to run or value to return when Option.SOME
        strict: if only Options should be expected

    Example:
        ```python
        import funml as ml

        some_value = ml.Option.SOME(90)
        none_value = ml.Option.NONE
        another_value = None

        # in case the value may not be an Option, set strict to False
        print(ml.if_some(str, strict=False)(another_value))
        # prints None

        some_to_str = ml.if_some(str)
        print(some_to_str(some_value))
        # prints 90

        print(some_to_str(none_value))
        # prints <Option.NONE: ('NONE',)>
        ```

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


def if_none(do: Union[Expression, Callable, Any], strict: bool = True) -> Expression:
    """Does the given operation if value passed to resulting expression is Option.NONE.

    If the value is Option.SOME, it just returns the Option.SOME without
    doing anything about it.

    Args:
        do: The expression, function, to run or value to return when Option.NONE
        strict: if only Options should be expected

    Example:
        ```python
        import funml as ml

        some_value = ml.Option.SOME(90)
        none_value = ml.Option.NONE
        another_value = None

        # in case the value may not be an Option, set strict to False
        print(ml.if_none(str, strict=False)(another_value))
        # prints None

        none_to_str = ml.if_none(str)
        print(none_to_str(some_value))
        # prints <Option.SOME: (90,)>

        print(none_to_str(none_value))
        # prints ('NONE',)
        ```

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


def is_ok(v: "Result", strict: bool = True) -> bool:
    """Checks if `v` is Result.OK.

    Args:
        v: The value to check
        strict: if value should be a Result

    Example:
        ```python
        import funml as ml

        ok_value = ml.Result.OK(90)
        err_value = ml.Result.ERR(TypeError())

        print(ml.is_ok(ok_value))
        # prints True

        print(ml.is_ok(err_value))
        # prints False

        another_value = None

        # in case the value is not always a Result, set `strict` to False
        # to avoid a MatchError
        print(ml.is_ok(another_value, strict=False))
        # prints False
        ```

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


def is_err(v: "Result", strict: bool = True) -> bool:
    """Checks if `v` is Result.ERR.

    Args:
        v: The value to check
        strict: if value should be a Result

    Example:
        ```python
        import funml as ml

        ok_value = ml.Result.OK(90)
        err_value = ml.Result.ERR(TypeError())

        print(ml.is_err(ok_value))
        # prints False

        print(ml.is_err(err_value))
        # prints True

        another_value = None

        # in case the value is not always a Result, set `strict` to False
        # to avoid a MatchError
        print(ml.is_err(another_value, strict=False))
        # prints False
        ```

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


def is_some(v: "Option", strict: bool = True) -> bool:
    """Checks if `v` is Option.SOME.

    Args:
        v: The value to check
        strict: if value should be a Option

    Example:
        ```python
        import funml as ml

        some_value = ml.Option.SOME(90)
        none_value = ml.Option.NONE

        print(ml.is_some(some_value))
        # prints True

        print(ml.is_some(none_value))
        # prints False

        another_value = None

        # in case the value is not always an Option, set `strict` to False
        # to avoid a MatchError
        print(ml.is_some(another_value, strict=False))
        # prints False
        ```

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


def is_none(v: "Option", strict: bool = True) -> bool:
    """Checks if `v` is Option.NONE.

    Args:
        v: The value to check
        strict: if value should be a Option

    Example:
        ```python
        import funml as ml

        some_value = ml.Option.SOME(90)
        none_value = ml.Option.NONE

        print(ml.is_none(some_value))
        # prints False

        print(ml.is_none(none_value))
        # prints True

        another_value = None

        # in case the value is not always an Option, set `strict` to False
        # to avoid a MatchError
        print(ml.is_none(another_value, strict=False))
        # prints False
        ```

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
