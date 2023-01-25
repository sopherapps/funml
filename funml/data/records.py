"""Records are map-like data structures

Results in something like:

Initializing a record is like:

>> Color = record(Color = {'r': int, 'g': int, 'b': int, a: int})

And utilizing the record:

>> blue = Color(r=0, g=0, b=255, a=1)
>> red = Color(r=255, g=0, b=0, a=1)
>> green = Color(r=0, g=255, b=0, a=1)
"""
from dataclasses import dataclass
from typing import Dict, Any

from funml import utils, types


def record(annotations: Dict[str, Any]):
    """creates a map-like data structure for storing related data, accessible by attribute"""

    record_name = utils.generate_random_string()
    return dataclass(
        type(
            record_name,
            (Record,),
            {"__annotations__": annotations, "__slots__": tuple(annotations.keys())},
        ),
        init=False,
    )


def _is_valid(kwargs: Dict[str, Any], annotations: Dict[str, Any]):
    """validates the key-word arguments passed to record when initializing"""
    if len(kwargs) > len(annotations):
        return False

    return all([utils.is_type(v, annotations.get(k, None)) for k, v in kwargs.items()])


class Record(types.MLType):
    """Base class for all Records"""

    def __init__(self, **kwargs: Any):
        self.__attrs = kwargs
        annotations = self.__annotations__
        if not _is_valid(kwargs, annotations):
            raise TypeError(
                f"expected key-word arguments of signature {annotations}, got {kwargs}"
            )

        for k, v in kwargs.items():
            setattr(self, k, v)

    def _is_like(self, other):
        """Checks that a value has the given pattern"""
        if not isinstance(other, Record) or self.__class__ != other.__class__:
            return False

        for k, v in self.__attrs.items():
            if getattr(other, k, None) != v:
                return False

        return True

    def generate_case(self, do: types.Operation):
        """Generates a case statement for pattern matching"""
        return self._is_like, types.Expression(
            types.Operation(func=lambda *args: do(*args))
        )
