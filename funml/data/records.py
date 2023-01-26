"""Schema types for similar records.

Typical Usage:

    ```python
    import funml as ml


    Color = ml.record({'r': int, 'g': int, 'b': int, 'a': int})
    blue = Color(r=0, g=0, b=255, a=1)
    red = Color(r=255, g=0, b=0, a=1)
    green = Color(r=0, g=255, b=0, a=1)

    print(blue)
    # prints: {'r': 0, 'g': 0, 'b': 255, 'a': 1}

    print(red)
    # prints: {'r': 255, 'g': 0, 'b': 0, 'a': 1}

    print(green)
    # prints: {'r': 0, 'g': 255, 'b': 0, 'a': 1}
    ```
"""
from dataclasses import dataclass
from typing import Dict, Any, Type, Callable, Tuple

from funml import utils, types


def record(annotations: Dict[str, Any]) -> Type["Record"]:
    """Creates a Schema type to create similar records.

    Creates a Schema for similar objects that contain a given
    set of attributes. For example, it can create a `Book` schema
    whose attributes include `author`, `title`, `isbn` etc.

    Args:
        annotations: a dict of the attributes and their data types

    Returns:
        A class/type whose attributes are the same as those passed as `annotations`.

    Example:
        ```python
        import funml as ml

        Color = ml.record({"red": int, "green": int, "blue": int})
        indigo = Color(red=75, green=0, blue=130)

        print(indigo)
        # prints {'red': 75, 'green': 0, 'blue': 130}
        ```
    """

    record_name = utils.generate_random_string()
    return dataclass(
        type(
            record_name,
            (Record,),
            {"__annotations__": annotations, "__slots__": tuple(annotations.keys())},
        ),
        init=False,
        repr=False,
    )


def _is_valid(kwargs: Dict[str, Any], annotations: Dict[str, Any]):
    """validates the key-word arguments passed to record when initializing"""
    if len(kwargs) > len(annotations):
        return False

    return all([utils.is_type(v, annotations.get(k, None)) for k, v in kwargs.items()])


class Record(types.MLType):
    """A Schema type for creating similar records.

    Basically, any unique record type subclasses Record, sets
    the expected attributes and then is used to create new instances
    of that record type.

    Args:
        kwargs: the data for the current record instance.

    Raises:
        TypeError: the data passed is does not correspond to the expected annotations.
    """

    def __init__(self, **kwargs: Any):
        self.__attrs = kwargs
        annotations = self.__annotations__
        if not _is_valid(kwargs, annotations):
            raise TypeError(
                f"expected key-word arguments of signature {annotations}, got {kwargs}"
            )

        for k, v in kwargs.items():
            setattr(self, k, v)

    def _is_like(self, other) -> bool:
        """See Base Class: [`MLType`][funml.types.MLType]"""
        if not isinstance(other, Record) or self.__class__ != other.__class__:
            return False

        for k, v in self.__attrs.items():
            if getattr(other, k, None) != v:
                return False

        return True

    def generate_case(self, do: types.Operation) -> Tuple[Callable, types.Expression]:
        """See Base Class: [`MLType`][funml.types.MLType]"""
        return self._is_like, types.Expression(
            types.Operation(func=lambda *args: do(*args))
        )

    def __str__(self):
        """A readable representation of this type."""
        return f"{self.__attrs}"
