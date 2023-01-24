"""funml is a functional-programming take on python
"""
from .lib import let, fn, match, val
from .data.enum import enum
from .data.monads import Option, Result
from .data.records import record
from .data.lists import l

__root__ = [let, fn, match, val, enum, Option, Result, record, l]
