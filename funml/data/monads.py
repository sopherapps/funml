"""Common monads

For more about monads, https://en.wikipedia.org/wiki/Monad_(functional_programming)
"""
from typing import Any

from .enum import enum

Option = enum("Option").opt("NONE").opt("SOME", shape=Any)
"""Represents a value that is potentially None

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


Result = enum("Result").opt("ERR", shape=Exception).opt("OK", shape=Any)
"""Represents a value that is potentially an exception

Example Usage:

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
