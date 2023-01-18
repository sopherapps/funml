"""Common monads

For more about monads, https://en.wikipedia.org/wiki/Monad_(functional_programming)
"""
from typing import Any

from .enum import enum, e

# Option represents a value that is potentially None
Option = enum(Option=e("NONE") | e("SOME").of((Any,)))


# Result represents a value that is potentially an exception
Result = enum(Option=e("ERR").of((Exception,)) | e("OK").of((Any,)))
