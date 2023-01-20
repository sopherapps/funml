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

from funml import utils


def record(**kwargs: Dict[str, Any]):
    """creates a map-like data structure for storing related data, accessible by attribute"""
    if len(kwargs) != 1:
        raise ValueError(f"required 1 key-word argument, got {len(kwargs)}")

    [(record_name, annotations)] = kwargs.items()
    return dataclass(
        type(
            record_name,
            (Record,),
            {"__annotations__": annotations, "__slots__": tuple(annotations.keys())},
        ),
        order=False,
        init=False,
    )


def _is_valid(kwargs: Dict[str, Any], annotations: Dict[str, Any]):
    """validates the key-word arguments passed to record when initializing"""
    if len(kwargs) > len(annotations):
        return False

    return all(
        [
            utils.is_type(kwargs.get(sig_key, None), sig_type)
            for sig_key, sig_type in annotations.items()
        ]
    )


class Record:
    """Base class for all Records"""

    def __init__(self, **kwargs: Any):
        annotations = self.__annotations__
        if not _is_valid(kwargs, annotations):
            raise TypeError(
                f"expected key-word arguments of signature {annotations}, got {kwargs}"
            )

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __le__(self, other: Any) -> bool:
        """'<=' is the match operator."""
        if isinstance(other, Record):
            return self == other
        return False
