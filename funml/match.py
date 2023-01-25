"""Pattern matching
"""
from typing import Any, Optional

from funml.types import MatchExpression


def match(arg: Optional[Any] = None) -> "MatchExpression":
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
                .case(l(str, 5, rest), do= fn(5)) \
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
    return MatchExpression(arg=arg)
