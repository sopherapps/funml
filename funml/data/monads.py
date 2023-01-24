"""Common monads

For more about monads, https://en.wikipedia.org/wiki/Monad_(functional_programming)
"""
from typing import Any

from .enum import enum

# Option represents a value that is potentially None
Option = enum("Option").opt("NONE").opt("SOME", shape=Any)


# Result represents a value that is potentially an exception
Result = enum("Result").opt("ERR", shape=Exception).opt("OK", shape=Any)
