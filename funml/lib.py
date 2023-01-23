"""The public API for funml"""
from functools import reduce
from typing import Type, Union, Callable, Any, Tuple

from .types import Assignment, Expression, _append_expn, _to_expn, MatchExpression


def let(
    t: Type,
    *args,
    **kwargs,
) -> Assignment:
    """Creates an assignment in a user-friendly way"""
    if len(args) == 1:
        return Assignment(var=args[0], t=t)
    elif len(kwargs) == 1:
        [(_var, _val)] = kwargs.items()
        return Assignment(var=_var, t=t) <= _val

    raise ValueError(f"kwargs passed should be only 1, got {len(kwargs)}")


def fn(*expressions: Union[Expression, Assignment, Callable, Any]) -> Expression:
    """Composes a new expression from other expression, moving from left to right"""
    if len(expressions) == 1:
        return _to_expn(expressions[0])
    return reduce(lambda a, b: _append_expn(a, b), expressions, val(None))


def val(v: Any):
    """val meaning value. Converts a generic value into a functional expression"""
    return _to_expn(v)


def match(arg: Any) -> "MatchExpression":
    """pattern matching using the match syntax

    Usage
    --
    # enums
    >> value = match(raw_value) \
            .case(Option.SOME(int), do=fn(lambda v: v + 6)) \
            .case(Option.NONE, do=fn())

    # records: use ... to capture value
    >> value2 = match(raw_value2)\
                .case(Color(r, g, ...), do=fn(lambda r, g: r + g)) \
                .case(ExamResult(total), do= fn(lambda v: v))

    # lists
    >> value3 = match(raw_value3) \
                .case(l(_, 5, rest), do= fn(5)) \
                .case(l(8, 5, rest), do= fn(rest))

    # combined
    >> value = match(raw_value) \
            .case(Option.SOME(int), do= fn(lambda v: v + 6)) \
            .case(Option.NONE, do= fn()) \
            .case(Color(r, g, ...), do= fn(lambda r, g: r + g))\
            .case(ExamResult(total), do= fn(lambda v: v)) \
            .case(l(_, 5, rest), do= fn(5)) \
            .case(l(8, 5, rest), do= fn(rest))
    """
    return MatchExpression(arg)
