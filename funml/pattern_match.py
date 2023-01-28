"""Pattern matching
"""
from typing import Any, Optional

from funml.types import MatchExpression


def match(arg: Optional[Any] = None) -> "MatchExpression":
    """Matches the argument with a corresponding case, and calls it `do` operation.

    It runs through a range of cases, looking for any that match
    the current arg. If it finds it, it calls the `do` operation attached
    to that case.

    Args:
        arg: the argument which is to be checked against the list of patterns.

    Returns:
        A [`MatchExpression`][funml.types.MatchExpression] containing the matched operation.

    Raises:
        MatchError: failed to find a match for the argument.

    Example:

        ```python
        import funml as ml

        @ml.record
        class Color:
            r: int
            g: int
            b: int

        raw_value = ml.Option.SOME(90)
        value = (
            ml.match(raw_value)
                .case(ml.Option.SOME(int), do=lambda v: v + 6)
                .case(ml.Option.NONE, do=lambda: "nothing to show")
                .case(Color(red=255), do=lambda v: v.red + v.green)
                .case(ml.l(..., 5), do=lambda v: v)
                .case(ml.l(8, 5, ...), do=lambda v: str(v))
        )()
        print(value)
        # prints 96
        ```
    """
    return MatchExpression(arg=arg)
