"""Enumerable user-defined data types

Typical Usage:

    ```python
    import funml as ml


    class Color(ml.Enum):
        RED = None
        BLUE = {'h': str, 's': str}
        GREEN = (int, str)
        ALPHA = float

    r = Color.RED
    g = Color.GREEN(6, "string")
    b = Color.BLUE({'h': 'when', 's': 'how'})
    a = Color.ALPHA(0.6)

    print(r)
    # prints: <Color.RED: ('RED',)>

    print(g)
    # prints: <Color.GREEN: (6, 'string')>

    print(b)
    # prints: <Color.BLUE: ({'h': 'when', 's': 'how'},)>

    print(a)
    # prints: <Color.ALPHA: 0.6>
    ```
"""
import json
from collections.abc import Iterable, Mapping
from typing import Type, Union, Tuple, Dict, Optional, Any, Callable

from funml import utils, types
from .records import Record
from ..utils import extract_type, right_pad_list


def _is_valid(
    value: Any,
    signature: Optional[Union[Tuple[Type, ...], Dict[str, Type], Type]],
) -> bool:
    """Checks to see if value is of given signature"""
    if signature is None:
        return True
    try:
        if isinstance(signature, tuple):
            return all([utils.is_type(v, sig) for sig, v in zip(signature, value)])
        elif isinstance(signature, dict):
            return all(
                [
                    utils.is_type(value.get(sig_key, None), sig_type)
                    for sig_key, sig_type in signature.items()
                ]
            )

        return utils.is_type(value, signature)
    except Exception:
        return False


class Enum(types.MLType):
    """Enumerable type that can only be in a limited number of forms.

    Other enums are created by inheriting from this type.
    An enum can only be in a limited number of forms or variant and each variant
    can have some data associated with each instance.

    Variants are created by setting class attributes. The value of the class
    attributes should be the shape of the associated data or `None` if variant has no
    associated data.

    The pre-created types of [`Option`][funml.Option] and [`Result`][funml.Result]
    are both enums

    Raises:
        TypeError: got unexpected data type, different from the signature

    Example:
        ```python
        import funml as ml
        from datetime import date

        class Day(ml.Enum):
            MON = date
            TUE = date
            WED = date
            THUR = date
            FRI = date
            SAT = date
            SUN = date

        dates =  [
            date(200, 3, 4),
            date(2009, 1, 16),
            date(1993, 12, 29),
            date(2004, 10, 13),
            date(2020, 9, 5),
            date(2004, 5, 7),
            date(1228, 8, 18),
        ]

        to_day_enum = lambda date_value: (
            ml.match(date_value.weekday())
                .case(0, do=lambda: Day.MON(date_value))
                .case(1, do=lambda: Day.TUE(date_value))
                .case(2, do=lambda: Day.WED(date_value))
                .case(3, do=lambda: Day.THUR(date_value))
                .case(4, do=lambda: Day.FRI(date_value))
                .case(5, do=lambda: Day.SAT(date_value))
                .case(6, do=lambda: Day.SUN(date_value))
        )()

        day_enums_transform = ml.imap(to_day_enum)
        day_enums = day_enums_transform(dates)

        print(day_enums)
        # prints [<Day.TUE: datetime.date(200, 3, 4)>, <Day.FRI: datetime.date(2009, 1, 16)>,\
        # <Day.WED: datetime.date(1993, 12, 29)>, <Day.WED: datetime.date(2004, 10, 13)>, \
        # <Day.SAT: datetime.date(2020, 9, 5)>, <Day.FRI: datetime.date(2004, 5, 7)>, \
        # <Day.FRI: datetime.date(1228, 8, 18)>]
        ```
    """

    signature: Optional[Union[Tuple[Type, ...], Dict[str, Type], Type]] = None
    _name: str = ""

    def __init_subclass__(cls, **kwargs):
        """Creating a new Enum"""
        slots = []

        for k, v in _get_cls_attrs(cls).items():
            cls.__add_variant(k, v)
            slots.append(k)

        cls.__slots__ = slots

    def __init__(self, *args: Union[Any, Dict[str, Any], int]):
        if isinstance(self.signature, tuple):
            data = args
        else:
            data = args[0]

        if not _is_valid(data, self.signature):
            raise TypeError(
                f"expected data type passed to be {self.signature}, got {data} from args: {args}"
            )

        self._value = data

    @classmethod
    def __add_variant(
        cls,
        name: str,
        shape: Optional[Union[Type, Tuple[Type, ...], Dict[str, Type]]] = None,
    ) -> Type["Enum"]:
        """Adds a given option to the enum.

        This is a chainable method that can be used to add multiple options
        to the same enum class.

        Args:
            name: the name of the option e.g. `ERR` for the [`Result`][funml.Result] enum
            shape: the signature of the associated data

        Returns:
             the Enum class to which the option has been attached.
        """
        dotted_name = f"{cls.__name__}.{name}"
        signature = shape

        if signature is None:
            opt_value = cls(name)
        else:
            # each option is a subclass of this enum class
            opt_value = type(dotted_name, (cls,), {})

        opt_value._name = dotted_name
        opt_value.signature = signature

        setattr(cls, name, opt_value)
        return cls

    @property
    def value(self):
        """The value associated with this Enum option, if any"""
        return self._value

    @property
    def name(self):
        """The name of this Enum"""
        return self._name

    def generate_case(self, do: types.Operation) -> Tuple[Callable, types.Expression]:
        """See Base Class: [`MLType`][funml.types.MLType]"""
        op = lambda *args: do(*args)
        if self._value is not None:
            op = lambda arg: do(_get_enum_captured_value(arg))

        return self._is_like, types.Expression(types.Operation(func=op))

    def _is_like(self, other) -> bool:
        """See Base Class: [`MLType`][funml.types.MLType]"""
        if not isinstance(other, Enum):
            return False

        return (
            self.__class__ == other.__class__
            and self._name == other._name
            and (self._value == other._value or _is_valid(other._value, self._value))
        )

    def __eq__(self, other: "Enum"):
        """Checks equality of the this enum and `other`.

        Args:
            other: the value to compare with current enum.
        """
        return (
            self.__class__ == other.__class__
            and self._name == other._name
            and utils.equals(self._value, other._value)
        )

    def __str__(self):
        """Generates a readable presentation of the enum."""
        return f"<{self.name}: {self.value}>"

    def __repr__(self):
        return f"<{self.name}: {self.value}>"


def _get_enum_captured_value(instance: Enum):
    """Gets the captured value for a given enum instance"""
    if isinstance(instance.signature, tuple) and len(instance.value) == 1:
        return instance.value[0]
    return instance.value


def _get_cls_attrs(cls: type) -> Dict[str, Any]:
    """Gets the attributes of the given class

    Args:
        cls: the class whose attributes are needed

    Returns:
        the class attributes as a dictionary
    """
    return {k: v for k, v in cls.__dict__.items() if not k.startswith("_")}
