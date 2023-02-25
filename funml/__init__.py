"""A collection of utilities to help write python as though it were an ML-kind of functional language like OCaml.

Provides:

1. Immutable data structures like enums, records, lists
2. Piping outputs of one function to another as inputs. That's how bigger functions are created from smaller ones.
3. Pattern matching for declarative conditional control of flow instead of using 'if's
4. Error handling using the `Result` monad, courtesy of [rust](https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html).
   Instead of using `try-except` all over the place, functions return
   a `Result` which has the right data when successful and an exception if unsuccessful.
   The result is then pattern-matched to retrieve the data or react to the exception.
5. No `None`. Instead, we use the `Option` monad, courtesy of [rust](https://doc.rust-lang.org/book/ch06-01-defining-an-enum.html?highlight=option#the-option-enum-and-its-advantages-over-null-values).
   When an Option has data, it is `Option.SOME`, or else it is `Option.NONE`.
   Pattern matching helps handle both scenarios.
"""
from .pattern_match import match
from .expressions import val
from .data.enum import Enum
from .data.monads import (
    Option,
    Result,
    if_ok,
    if_err,
    if_none,
    if_some,
    is_err,
    is_none,
    is_ok,
    is_some,
)
from .data.records import record, to_dict, Record
from .data.lists import l, imap, ifilter, ireduce
from .pipeline import execute
from .json import to_json, from_json

__all__ = [
    "match",
    "val",
    "Enum",
    "Option",
    "Result",
    "if_ok",
    "if_err",
    "if_some",
    "if_none",
    "is_ok",
    "is_err",
    "is_some",
    "is_none",
    "record",
    "Record",
    "to_dict",
    "to_json",
    "from_json",
    "l",
    "imap",
    "ifilter",
    "ireduce",
    "errors",
    "types",
    "data",
    "execute",
]
