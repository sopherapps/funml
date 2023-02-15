"""Schema types for similar records.

Typical Usage:

    ```python
    import funml as ml

    @ml.record
    class Color:
        r: int
        g: int
        b: int
        a: int = 1

    blue = Color(r=0, g=0, b=255, a=1)
    red = Color(r=255, g=0, b=0, a=1)
    green = Color(r=0, g=255, b=0)

    print(blue)
    # prints: {'r': 0, 'g': 0, 'b': 255, 'a': 1}

    print(red)
    # prints: {'r': 255, 'g': 0, 'b': 0, 'a': 1}

    print(green)
    # prints: {'r': 0, 'g': 255, 'b': 0, 'a': 1}
    ```
"""
import dataclasses
from typing import Dict, Any, Type, Callable, Tuple, TypeVar

from typing_extensions import dataclass_transform

from funml import utils, types


R = TypeVar("R", bound="Record")


def to_dict(v: "Record") -> Dict[str, Any]:
    """Converts a record into a dictionary.

    Args:
        v: the `Record` to convert to dict

    Returns:
        the dictionary representation of the record
    """
    return dataclasses.asdict(v)


@dataclass_transform(
    field_specifiers=(dataclasses.Field, dataclasses.field),
)
def record(cls: Type[R]) -> Type[R]:
    """Creates a Schema type to create similar records.

    Used usually as a decorator inplace of @dataclass
    on dataclass-like classes to make them ml-functional.

    It creates a Schema for similar objects that contain a given
    set of attributes. For example, it can create a `Book` schema
    whose attributes include `author`, `title`, `isbn` etc.

    Args:
        cls: the class to transform into a record

    Returns:
        A class which can act as a record of the particular schema \
        set by the attributes.

    Example:
        ```python
        import funml as ml

        @ml.record
        class Color:
            red: int
            green: int
            blue: int
            alpha: int = 1

        indigo = Color(red=75, green=0, blue=130)

        print(indigo)
        # prints {'red': 75, 'green': 0, 'blue': 130, 'alpha': 1}
        ```
    """
    annotations = utils.get_cls_annotations(cls, eval_str=True)
    defaults = utils.get_cls_defaults(cls, annotations=annotations)

    return dataclasses.dataclass(
        type(
            cls.__name__,
            (Record,),
            {
                "__annotations__": annotations,
                "__slots__": tuple(annotations.keys()),
                "__dataclass_fields__": annotations,
                "__defaults__": defaults,
            },
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

    This type is usually not used directly but rather we use the [@record](funml.record) decorator

    Example:

        ```python
        import funml as ml

        @ml.record
        class Color:
            r: int
            g: int
            b: int
            a: int = 1
        ```

    Args:
        kwargs: the data for the current record instance.

    Raises:
        TypeError: the data passed is does not correspond to the expected annotations.
    """

    __defaults__: Dict[str, Any] = {}

    def __init__(self, **kwargs: Any):
        kwargs = {**self.__defaults__, **kwargs}
        self.__attrs = kwargs

        if not _is_valid(kwargs, self.__annotations__):
            raise TypeError(
                f"expected key-word arguments of signature {self.__annotations__}, got {kwargs}"
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
